"""Process specific chat files through chat -> repo -> single file pipeline."""
import os
from chat_to_repo import ChatToRepoConverter
from repo_to_single_file import RepoToSingleFileConverter


def process_specific_chats():
    chat_directory = "/Users/jo/Downloads/docs/chatgpt-export-markdown"
    
    target_files = [
        "ChatGPT-500$_Art_Selling_Tips.md",
        "ChatGPT-Abstract_Landscape_Description.pdf",
        "ChatGPT-Account_and_File_Inquiry.md",
    ]
    
    chat_converter = ChatToRepoConverter()
    repo_converter = RepoToSingleFileConverter()
    all_repo_files = []
    
    for filename in target_files:
        filepath = os.path.join(chat_directory, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} - file not found")
            continue
        if filename.endswith('.pdf'):
            print(f"Skipping {filename} - PDF not supported")
            continue
        try:
            chat_file = chat_converter.parse_chat_file(filepath)
            repo_files = chat_converter.convert_chat_to_repo_structure(chat_file)
            all_repo_files.extend(repo_files)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    if all_repo_files:
        combined_content = repo_converter.convert_repo_to_single_file(all_repo_files)
        output_path = "/Users/jo/Desktop/eee/overworker/combined_chat_repo.txt"
        repo_converter.write_combined_file(combined_content, output_path)
        print(f"Combined file written to: {output_path}")


if __name__ == "__main__":
    process_specific_chats()
