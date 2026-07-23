"""
Language data loader utility.
Handles loading and managing language resources (dictionary, phrases, grammar).
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class LanguageLoader:
    """Loads and manages language learning resources."""
    
    def __init__(self, base_path: str = "languages"):
        self.base_path = Path(base_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load the languages configuration."""
        config_path = self.base_path / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"supported_languages": [], "default_language": None}
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return [
            lang for lang in self.config.get("supported_languages", [])
            if lang.get("enabled", True)
        ]
    
    def load_language_data(self, language_code: str) -> Dict[str, Any]:
        """
        Load all data for a specific language.
        
        Args:
            language_code: The language code (e.g., 'bambili')
            
        Returns:
            Dictionary containing all language data
        """
        lang_path = self.base_path / language_code
        
        if not lang_path.exists():
            raise ValueError(f"Language '{language_code}' not found")
        
        data = {}
        
        # Load metadata
        metadata_path = lang_path / "metadata.json"
        if metadata_path.exists():
            data["metadata"] = self._load_json(metadata_path)
        
        # Load dictionary
        dict_path = lang_path / "dictionary.json"
        if dict_path.exists():
            data["dictionary"] = self._load_json(dict_path)
        
        # Load phrases
        phrases_path = lang_path / "phrases.json"
        if phrases_path.exists():
            data["phrases"] = self._load_json(phrases_path)
        
        # Load grammar
        grammar_path = lang_path / "grammar.json"
        if grammar_path.exists():
            data["grammar"] = self._load_json(grammar_path)
        
        return data
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load a JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def save_dictionary_entry(self, language_code: str, category: str, 
                            english: str, translation: str) -> bool:
        """
        Add a new dictionary entry.
        
        Args:
            language_code: The language code
            category: Category in dictionary (e.g., 'basic_words', 'nouns')
            english: English word/phrase
            translation: Translation in target language
            
        Returns:
            True if successful
        """
        dict_path = self.base_path / language_code / "dictionary.json"
        
        if not dict_path.exists():
            return False
        
        with open(dict_path, "r", encoding="utf-8") as f:
            dictionary = json.load(f)
        
        # Ensure category exists
        if category not in dictionary:
            dictionary[category] = {}
        
        # Add entry
        dictionary[category][english.lower().strip()] = translation.strip()
        
        # Save back
        with open(dict_path, "w", encoding="utf-8") as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)
        
        return True
    
    def save_grammar_entry(self, language_code: str, category: str, 
                          english: str, translation: str) -> bool:
        """
        Add a new grammar entry (pronouns or verbs).
        
        Args:
            language_code: The language code
            category: Category in grammar (e.g., 'pronouns', 'verbs')
            english: English word/phrase
            translation: Translation in target language
            
        Returns:
            True if successful
        """
        grammar_path = self.base_path / language_code / "grammar.json"
        
        if not grammar_path.exists():
            return False
        
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = json.load(f)
        
        # Ensure category exists
        if category not in grammar:
            grammar[category] = {}
        
        # Add entry
        grammar[category][english.lower().strip()] = translation.strip()
        
        # Save back
        with open(grammar_path, "w", encoding="utf-8") as f:
            json.dump(grammar, f, indent=2, ensure_ascii=False)
        
        return True
    
    def get_total_words(self, language_code: str) -> int:
        """Get total number of words in dictionary and grammar."""
        data = self.load_language_data(language_code)
        dictionary = data.get("dictionary", {})
        grammar = data.get("grammar", {})
        
        total = 0
        
        # Count dictionary entries
        for category in dictionary.values():
            if isinstance(category, dict):
                total += len(category)
        
        # Count grammar entries (pronouns and verbs)
        for category_name in ["pronouns", "verbs"]:
            if category_name in grammar and isinstance(grammar[category_name], dict):
                total += len(grammar[category_name])
        
        return total
    
    def search_word(self, language_code: str, english_word: str) -> Optional[str]:
        """
        Search for a word translation in dictionary and grammar.
        
        Args:
            language_code: The language code
            english_word: The English word to search for
            
        Returns:
            Translation if found, None otherwise
        """
        data = self.load_language_data(language_code)
        dictionary = data.get("dictionary", {})
        grammar = data.get("grammar", {})
        
        english_lower = english_word.lower().strip()
        
        # Search in dictionary categories
        for category in dictionary.values():
            if isinstance(category, dict) and english_lower in category:
                return category[english_lower]
        
        # Search in grammar categories (pronouns and verbs)
        for category_name in ["pronouns", "verbs"]:
            if category_name in grammar and isinstance(grammar[category_name], dict):
                if english_lower in grammar[category_name]:
                    return grammar[category_name][english_lower]
        
        return None
    
    def format_for_ai_context(self, language_code: str) -> str:
        """
        Format all language data for AI context injection.
        
        Args:
            language_code: The language code
            
        Returns:
            Formatted string for AI prompt
        """
        data = self.load_language_data(language_code)
        
        context_parts = []
        
        # Add metadata
        if "metadata" in data:
            meta = data["metadata"]
            context_parts.append(f"LANGUAGE: {meta.get('language_name', language_code)}")
            context_parts.append(f"REGION: {meta.get('region', 'Unknown')}")
            context_parts.append(f"DESCRIPTION: {meta.get('description', 'No description')}")
            context_parts.append("")
        
        # Add dictionary
        if "dictionary" in data:
            context_parts.append("DICTIONARY:")
            context_parts.append(json.dumps(data["dictionary"], indent=2, ensure_ascii=False))
            context_parts.append("")
        
        # Add phrases
        if "phrases" in data:
            context_parts.append("COMMON PHRASES:")
            context_parts.append(json.dumps(data["phrases"], indent=2, ensure_ascii=False))
            context_parts.append("")
        
        # Add grammar
        if "grammar" in data:
            context_parts.append("GRAMMAR RULES:")
            context_parts.append(json.dumps(data["grammar"], indent=2, ensure_ascii=False))
            context_parts.append("")
        
        return "\n".join(context_parts)
