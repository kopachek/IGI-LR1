import re
import zipfile
import os

class BaseAnalyzer:
    def __init__(self, text):
        self.text = text
        self.sentences = re.findall(r'[^.!?]+[.!?]', text)
        self.words = re.findall(r'\b[a-zA-Zа-яА-Я]+\b', text)

    def get_report(self):
        """Base statistics"""
        declarative = len(re.findall(r'[^.!?]+\.', self.text))
        interrogative = len(re.findall(r'[^.!?]+\?', self.text))
        exclamatory = len(re.findall(r'[^.!?]+\!', self.text))
        
        avg_sent_len = sum(len(s) for s in self.sentences) / len(self.sentences) if self.sentences else 0
        avg_word_len = sum(len(w) for w in self.words) / len(self.words) if self.words else 0

        return {
            "total_sentences": len(self.sentences),
            "types": {"narrative": declarative, "interrogative": interrogative, "exclamatory": exclamatory},
            "avg_sentence_len": round(avg_sent_len),
            "avg_word_len": round(avg_word_len),
            "smileys_count": self.count_smileys()
        }
    
    def count_smileys(self):
        pattern = r'[;:][-]*([()\[\]])\1*'
        return len([m for m in re.finditer(pattern, self.text)])

class VariantAnalyzer(BaseAnalyzer):
    def get_report(self):
        """An extended report with variant tasks"""
        report = super().get_report()
        report.update({
            "lowercase_words": self.get_lowercase(),
            "punctuation_marks": self.get_punctuation(),
            "mac_valid": self.check_mac(),
            "consonant_words": self.count_consonant_words(),
            "double_letters": self.find_double_letters(),
            "alphabetic_unique_words": self.alphabetic_words()
        })
        return report
    
    def get_lowercase(self):
        words_pattern = r'\b[a-zа-яё]\w*\b'
        lower_words = re.findall(words_pattern, self.text)
        return lower_words
    
    def get_punctuation(self):
        punct_pattern = r'[^\w\s]'
        punctuation = re.findall(punct_pattern, self.text)
        return punctuation

    def check_mac(self):
        pattern = r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}'
        return bool(re.match(pattern, self.text.strip()))

    def count_consonant_words(self):
        pattern = r'\b[bcdfghjklmnpqrstvwxyzбвгджзйклмнпрстфхцчшщ]\w*'
        return len(re.findall(pattern, self.text, re.IGNORECASE))

    def find_double_letters(self):
        pattern = r'\b\w*(\w)\1\w*\b'
        matches = []
        for i, word in enumerate(self.words, 1):
            if re.search(pattern, word, re.IGNORECASE):
                matches.append(f"{word} (№{i})")
        return matches
    
    def alphabetic_words(self):
        sorted_words = sorted(list(set(self.words)), key=str.lower)
        return sorted_words

def task_2(input_file, output_file, zip_name):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    analyzer = VariantAnalyzer(content)
    results = analyzer.get_report()

    with open(output_file, 'w', encoding='utf-8') as f:
        for key, val in results.items():
            f.write(f"{key}: {val}\n")

    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        short_name = os.path.basename(output_file) 
        z.write(output_file, arcname=short_name)

    with zipfile.ZipFile(zip_name, 'r') as z:
        info = z.getinfo(short_name)
        print(f"File in zip: {info.filename}, Size: {info.file_size} bytes")

if __name__ == "__main__":
    task_2("T2\\init.txt","T2\\res.txt","T2\\archive.zip")