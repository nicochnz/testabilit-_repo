import os
import shutil
from abc import ABC, abstractmethod


class FileSystem(ABC):
    @abstractmethod
    def exists(self, path):
        pass

    @abstractmethod
    def copy(self, src, dst):
        pass

    @abstractmethod
    def move(self, src, dst):
        pass

    @abstractmethod
    def delete_file(self, path):
        pass

    @abstractmethod
    def delete_directory(self, path):
        pass


class OSFileSystem(FileSystem):
    def exists(self, path):
        return os.path.exists(path)

    def copy(self, src, dst):
        shutil.copy2(src, dst)

    def move(self, src, dst):
        shutil.move(src, dst)

    def delete_file(self, path):
        os.remove(path)

    def delete_directory(self, path):
        shutil.rmtree(path)


class FileExplorer:
    def __init__(self, start_path):
        self.current_path = start_path

    def list_directory(self):
        return os.listdir(self.current_path)

    def display_directory_contents(self):
        contents = self.list_directory()
        print(f"\nCurrent Directory: {self.current_path}")
        print("-" * 50)
        for index, element in enumerate(contents):
            full_path = os.path.join(self.current_path, element)
            element_type = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
            print(f"{index}. {element_type}: {element}")

    def navigate(self, index):
        contents = self.list_directory()
        selected = contents[index]
        full_path = os.path.join(self.current_path, selected)
        if os.path.isdir(full_path):
            self.current_path = full_path
        else:
            print("Cannot navigate into a file")

    def go_to_parent_directory(self):
        self.current_path = os.path.dirname(self.current_path)


class FileSelector:
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        self.current_directory_contents = os.listdir(directory_path)
        return self.current_directory_contents

    def select_files_by_indices(self, indices, directory_path):
        selected_indices = [int(i.strip()) for i in indices.split(',')]
        self.selected_files.clear()

        for index in selected_indices:
            if 0 <= index < len(self.current_directory_contents):
                full_path = os.path.join(
                    directory_path,
                    self.current_directory_contents[index]
                )
                self.selected_files.append(full_path)

        print("Selected files:")
        for file in self.selected_files:
            print(f" - {os.path.basename(file)}")

        return self.selected_files

    def get_selected_files(self):
        return self.selected_files

    def clear_selection(self):
        self.selected_files.clear()


class FileManager:
    def __init__(self, file_system, file_selector):
        self.file_system = file_system
        self.file_selector = file_selector

    def copy_files(self, destination):
        selected_files = self.file_selector.get_selected_files()
        for file in selected_files:
            if self.file_system.exists(file):
                self.file_system.copy(file, destination)
        print(f"{len(selected_files)} file(s) copied")
        self.file_selector.clear_selection()

    def move_files(self, destination):
        selected_files = self.file_selector.get_selected_files()
        for file in selected_files:
            if self.file_system.exists(file):
                self.file_system.move(file, destination)
        print(f"{len(selected_files)} file(s) moved")
        self.file_selector.clear_selection()

    def delete_files(self):
        selected_files = self.file_selector.get_selected_files()
        for file in selected_files:
            if os.path.isfile(file):
                self.file_system.delete_file(file)
            elif os.path.isdir(file):
                self.file_system.delete_directory(file)
        print(f"{len(selected_files)} file(s)/folder(s) deleted")
        self.file_selector.clear_selection()


def main_menu():
    explorer = FileExplorer(os.path.expanduser('~'))
    file_selector = FileSelector()
    file_system = OSFileSystem()
    file_manager = FileManager(file_system, file_selector)

    while True:
        print("\n--- File Explorer ---")
        print("1. Display Directory")
        print("2. Navigate")
        print("3. Go to Parent Directory")
        print("4. Select Files")
        print("5. Copy")
        print("6. Move")
        print("7. Delete")
        print("8. Quit")

        choice = input("Your choice: ")

        if choice == '1':
            explorer.display_directory_contents()

        elif choice == '2':
            index = int(input("Enter navigation index: "))
            explorer.navigate(index)
            explorer.display_directory_contents()

        elif choice == '3':
            explorer.go_to_parent_directory()
            explorer.display_directory_contents()

        elif choice == '4':
            explorer.display_directory_contents()
            file_selector.load_directory_contents(explorer.current_path)
            indices = input("Enter file indices to select (comma-separated): ")
            file_selector.select_files_by_indices(indices, explorer.current_path)

        elif choice == '5':
            dest = input("Enter destination path for copying: ")
            file_manager.copy_files(dest)

        elif choice == '6':
            dest = input("Enter destination path for moving: ")
            file_manager.move_files(dest)

        elif choice == '7':
            file_manager.delete_files()

        elif choice == '8':
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main_menu()
