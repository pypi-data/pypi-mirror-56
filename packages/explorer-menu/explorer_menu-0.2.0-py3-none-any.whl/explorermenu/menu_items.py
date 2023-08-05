import re
import winreg
import warnings
from typing import List, Union

_BACKGROUND_PATH = r'Software\Classes\Directory\Background'
_LIBRARY_PATH = r'Software\Classes\LibraryFolder\Background'


class _LabelValuePair:
    def __init__(self, label: str, value: str) -> None:
        self.label = label
        self.value = value


class _MenuItem:
    def __init__(self,
                 label: str,
                 children: List['_MenuItem'],
                 label_values: List[_LabelValuePair],
                 subkey_path: str = None
                 ) -> None:
        def label_to_subkey(label_: str) -> str:
            return re.sub(r'\W+', '_', label_).lower()
        self.children = children if children else []
        self.label = label
        self.subkey_path = subkey_path if subkey_path else f'shell\\{label_to_subkey(label)}'
        self.label_values = label_values

    def add_child(self, child: '_MenuItem') -> None:
        if isinstance(child, _MenuItem):
            self.children.append(child)

    def register(self) -> None:
        def register_at(root_shell: str, label_values: List[_LabelValuePair], subkey_path: str):
            subkey = '\\'.join([root_shell, subkey_path])
            item = winreg.CreateKey(winreg.HKEY_CURRENT_USER, subkey)
            for i in label_values:
                winreg.SetValueEx(item, i.label, 0, winreg.REG_SZ, i.value)
            winreg.FlushKey(item)

        register_at(_BACKGROUND_PATH, self.label_values, self.subkey_path)
        register_at(_LIBRARY_PATH, self.label_values, self.subkey_path)

        for child in self.children:
            new_subkey_path = '\\'.join(filter(None, [self.subkey_path, child.subkey_path]))
            child.subkey_path = new_subkey_path
            child.register()

    def remove(self) -> None:
        def remove_from(root: int, subkey: str):
            try:
                hkey = winreg.OpenKey(root, subkey, access=winreg.KEY_ALL_ACCESS)
            except OSError:
                return
            while True:
                try:
                    child = winreg.EnumKey(hkey, 0)
                except OSError:
                    break
                remove_from(hkey, child)
            winreg.CloseKey(hkey)
            winreg.DeleteKey(root, subkey)

        remove_from(winreg.HKEY_CURRENT_USER, f'{_BACKGROUND_PATH}\\{self.subkey_path}')
        remove_from(winreg.HKEY_CURRENT_USER, f'{_LIBRARY_PATH}\\{self.subkey_path}')


class MenuContainerItem(_MenuItem):
    def __init__(self, label: str, children: List[_MenuItem] = None) -> None:
        mui_verb = _LabelValuePair('MUIVerb', label)
        subcommands = _LabelValuePair('subcommands', '')
        label_values = [
            mui_verb,
            subcommands
        ]
        super().__init__(label, children, label_values)


class MenuActionItem(_MenuItem):
    def __init__(self, label: str, command: str) -> None:
        self.command = command
        command_pair = _LabelValuePair('', self.command)
        command_menu_item = _MenuItem('', [], [command_pair], '\\command')
        children = [command_menu_item]
        label_values = [_LabelValuePair('', label)]
        super().__init__(label, children, label_values)

    def add_child(self, child) -> None:
        warnings.warn("MenuActionItem wont add children")


def node(label: str, *children_or_command: Union[str, _MenuItem]) -> Union[MenuActionItem, MenuContainerItem]:
    is_action = len(children_or_command) == 1 and isinstance(children_or_command[0], str)

    if is_action:
        command = children_or_command[0]
        return MenuActionItem(label, command)

    if all(isinstance(child, _MenuItem) for child in children_or_command):
        children = list(children_or_command)
    else:
        children = []

    return MenuContainerItem(label, children)

