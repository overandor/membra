"""Chat to repository converter - converts ChatGPT exports to repo structure."""
import os
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    role: str  # 'You', 'ChatGPT', 'Assistant'
    content: str
    timestamp: str


@dataclass
class ChatFile:
    filename: str
    title: str
    messages: List[ChatMessage]
    metadata: Dict


class ChatToRepoConverter:
    """Converts ChatGPT conversation exports to repository structure."""
    
    def __init__(self):
        self.chat_files: List[ChatFile] = []
    
    def parse_chat_file(self, filepath: str) -> ChatFile:
        """Parse a single ChatGPT export file."""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else os.path.basename(filepath)
        
        messages = []
        current_role = None
        current_content = []
        
        for line in lines[1:]:
            if line.startswith('#### '):
                if current_role and current_content:
                    messages.append(ChatMessage(
                        role=current_role,
                        content='\n'.join(current_content).strip(),
                        timestamp=datetime.utcnow().isoformat()
                    ))
                role_match = re.search(r'####\s*(.+?):', line)
                current_role = role_match.group(1) if role_match else 'Unknown'
                current_content = []
            elif current_role:
                current_content.append(line)
        
        if current_role and current_content:
            messages.append(ChatMessage(
                role=current_role,
                content='\n'.join(current_content).strip(),
                timestamp=datetime.utcnow().isoformat()
            ))
        
        return ChatFile(
            filename=os.path.basename(filepath),
            title=title,
            messages=messages,
            metadata={
                "source_path": filepath,
                "message_count": len(messages),
                "total_chars": sum(len(m.content) for m in messages)
            }
        )
    
    def convert_chat_to_repo_structure(self, chat_file: ChatFile) -> List[Tuple[str, str]]:
        """Convert a chat file into repository file structure."""
        files = []
        
        conv_content = f"# {chat_file.title}\n\n"
        for msg in chat_file.messages:
            conv_content += f"## {msg.role}\n\n{msg.content}\n\n"
        
        files.append((
            f"conversations/{chat_file.filename}",
            conv_content
        ))
        
        you_messages = [m for m in chat_file.messages if 'You' in m.role]
        assistant_messages = [m for m in chat_file.messages if 'ChatGPT' in m.role or 'Assistant' in m.role]
        
        if you_messages:
            you_content = f"# User Messages from {chat_file.title}\n\n"
            for msg in you_messages:
                you_content += f"{msg.content}\n\n---\n\n"
            files.append((
                f"user_inputs/{chat_file.filename.replace('.md', '_user.md')}",
                you_content
            ))
        
        if assistant_messages:
            assistant_content = f"# Assistant Responses from {chat_file.title}\n\n"
            for msg in assistant_messages:
                assistant_content += f"{msg.content}\n\n---\n\n"
            files.append((
                f"assistant_responses/{chat_file.filename.replace('.md', '_assistant.md')}",
                assistant_content
            ))
        
        return files
    
    def batch_convert(self, chat_directory: str) -> List[Tuple[str, str]]:
        """Convert all chat files in a directory to repo structure."""
        all_files = []
        
        for filename in os.listdir(chat_directory):
            if filename.startswith('ChatGPT-') and filename.endswith('.md'):
                filepath = os.path.join(chat_directory, filename)
                try:
                    chat_file = self.parse_chat_file(filepath)
                    repo_files = self.convert_chat_to_repo_structure(chat_file)
                    all_files.extend(repo_files)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return all_files
