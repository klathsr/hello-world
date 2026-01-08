"""
Chawanagorn Thiangsiri
673040660-7
Lab4-3 P1
"""

from datetime import datetime


class LibraryItem:
    def __init__(self,title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False

    def get_status(self):
        return "Checked out" if self._checked_out else "Available"
    
    def check_out(self):
        # if checked_out is False (item still in lib)
        if not self._checked_out:
            self._checked_out = True
            return True
        # can't check out if item not in lib
        return False
    
    def display_info(self):
        print(f"Item: {self.title}")
        print(f" ID: {self._id}")
        print(f"status: {self.get_status()}")


class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0

    def set_page_count(self, pages):
        self.pages_count = pages

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Status: {self.get_status()}")
    

class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level
    
    def display_info(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")
        print(f"Status: {self.get_status()}")

class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number
        now = datetime.now()
        self.month = now.month
        self.year = now.year
    
    def display_issue(self):
        print(f"Title: {self.title}")
        print(f"Issue Number: {self.issue_number}")
        print(f"Date: {self.month}/{self.year}")
        print(f"Status: {self.get_status()}")

book = Book("Harry Potter", "B001", "J.K. Rowling")
book.set_page_count(500)
book.check_out()
book.display_info()

print("\nTesting TextBook:")
textbook = TextBook("Math", "T1", "ronaldo", "Math", "Grade 1")
textbook.set_page_count(300)
textbook.display_info()
textbook.check_out()
textbook.display_info()

print("\nTesting Magazine:")
magazine = Magazine("football", "cr7", "Lm10")
magazine.display_issue() 
magazine.check_out()
magazine.display_issue() 
        