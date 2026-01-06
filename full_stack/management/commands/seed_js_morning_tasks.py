from django.core.management.base import BaseCommand
from full_stack.models import Language, Concept, Task
from django.db import transaction

class Command(BaseCommand):
    help = "Seed JavaScript Morning Tasks"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 1️⃣ Create / Get Language
        language, _ = Language.objects.get_or_create(name="Java Script")

        # 2️⃣ Create / Get Concept
        concept, _ = Concept.objects.get_or_create(
            language=language,
            name="Morning Tasks - JS"
        )

        tasks = [
            "Find area of a circle (area = π × r × r) ,Find perimeter of a circle (perimeter = 2 × π × r)",

            "i) Find compound interest (CI = p × (1 + r/100)^t − p), ii)Convert Celsius to Fahrenheit (F = (C × 9/5) + 32)",

            "Check eligible to vote using ternary operator, Find largest of two numbers using ternary operator, Find smallest of three numbers using operators,Check positive or negative number,Check pass or fail using ternary operator", 
            
            "The electricity bill is calculated based on the number of units consumed. Different rates are applied for different unit slabs. Units from 0–100 are charged at ₹1.50 per unit. Units from 101–200 are charged at ₹2.50 per unit. Units from 201–300 are charged at ₹4.00 per unit. Units above 300 are charged at ₹5.00 per unit. The total bill is calculated by adding the charges from each slab."

            "Check if a triangle is valid / isosceles / equilateral / scalene",

            "Time-based greeting (morning, afternoon, evening, night)",

            "Scholarship eligibility based on marks and income",
            
            "Print sum of numbers from 1 to N",
            
            "Find the factorial of a number",

            "Print all prime numbers between 1 and 100",

            "Reverse a string and check if it is a palindrome",
            
            "Count vowels and consonants in a string",
            "Count occurrences of a specific character",
            
            "Find the largest and smallest word in a sentence",
            "Reverse each word in a sentence",

            "Count digits in a number",
            "Reverse a number and check if it is a palindrome",
            "Calculate sum of digits of a number",

            "Find largest and smallest element in an array",
            "Sort an array in ascending order without using .sort()",
            "Count even and odd numbers in an array and find their sum",
            "Remove duplicates from an array without built-in functions",
            "Reverse an array without built-in functions",
            "Search a number in an array without built-in methods",
            "Merge two arrays without using .concat() and find sum",
            "Check if an element exists in an array and print index",
            "Count frequency of each element in an array",

            "Count words and character frequency (excluding spaces) and return object",
            "Check if two strings are anagrams",
            "Capitalize first letter of each word / title case",
            "Remove whitespace from a string",
            "Remove digits from a string",
            "Remove special characters from a string",
            "Remove duplicate characters in a string",
            "Find the most repeated character in a string",
        ]

        # 3️⃣ Prevent duplicates
        existing_tasks = set(
            Task.objects.filter(concept=concept)
            .values_list("description", flat=True)
        )

        created_count = 0

        for task in tasks:
            if task not in existing_tasks:
                Task.objects.create(
                    concept=concept,
                    description=task
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {created_count} JavaScript Morning Tasks seeded successfully!"
            )
        )
