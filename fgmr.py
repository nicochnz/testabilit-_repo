import os
import shutil

""" File Manager Console Application 
    Refactored for testability – Step 1 (SRP)
"""


class FileSelector:
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        try:
            self.current_directory_contents = os.listdir(directory_path)
            return self.current_directory_contents
        except Exception as e:
            print(f"Error loading directory contents: {e}")
            return []

    def select_files_by_indices(self, indices, directory_path):
        try:
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
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []

    def get_selected_files(self):
        return self.selected_files

    def clear_selection(self):
        self.selected_files.clear()


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


class FileManager:
    def __init__(self, explorer, file_selector):
        self.explorer = explorer
        self.file_selector = file_selector

    def copy_files(self, destination):
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.copy2(file, destination)
            print(f"{len(selected_files)} file(s) copied")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Copy error: {e}")

    def move_files(self, destination):
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.exists(file):
                    shutil.move(file, destination)
            print(f"{len(selected_files)} file(s) moved")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Move error: {e}")

    def delete_files(self):
        try:
            selected_files = self.file_selector.get_selected_files()
            for file in selected_files:
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
            print(f"{len(selected_files)} file(s)/folder(s) deleted")
            self.file_selector.clear_selection()
        except Exception as e:
            print(f"Delete error: {e}")


def main_menu():
    explorer = FileExplorer(os.path.expanduser('~'))
    file_selector = FileSelector()
    file_manager = FileManager(explorer, file_selector)

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

        try:
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

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main_menu()
