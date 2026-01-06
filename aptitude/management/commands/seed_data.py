from django.core.management.base import BaseCommand
from aptitude.models import Concept, Question


class Command(BaseCommand):
    help = "Seed initial data with fresh Percentage questions"

    def handle(self, *args, **kwargs):

        # 1️⃣ Create Concept
        

        # 3️⃣ Practice Questions (19 new questions)


        data = [
            {
                "concept": "Profit & Loss",
                "questions": [
                    {
                        "question": "A shopkeeper buys a watch for ₹800 and sells it for ₹1,000. What is the profit percentage?",
                        "correct_answer": "25%",
                        "explanation": "Profit = 200 → (200/800) × 100 = 25%",
                        "is_demo": False,
                        "order": 1
                    },
                    {
                        "question": "A shirt marked at ₹600 is sold at a discount of 15%. What is the selling price?",
                        "correct_answer": "₹510",
                        "explanation": "15% of 600 = 90 → SP = 600 − 90 = 510",
                        "is_demo": False,
                        "order": 2
                    },
                    {
                        "question": "A man bought an item for ₹750 and sold it at 10% loss. What is the selling price?",
                        "correct_answer": "₹675",
                        "explanation": "Loss = 10% of 750 = 75 → SP = 750 − 75 = 675",
                        "is_demo": False,
                        "order": 3
                    },
                    {
                        "question": "A trader sells two items at profit of 20% and 30%. If both cost ₹500 each, what is total selling price?",
                        "correct_answer": "₹1150",
                        "explanation": "500×1.2 + 500×1.3 = 600 + 650 = 1150",
                        "is_demo": False,
                        "order": 4
                    },
                    {
                        "question": "A pen bought for ₹50 is sold for ₹65. What is the profit percentage?",
                        "correct_answer": "30%",
                        "explanation": "Profit = 15 → (15/50) × 100 = 30%",
                        "is_demo": False,
                        "order": 5
                    },
                ]
            },
            {
                "concept": "Simple Interest",
                "questions": [
                    {
                        "question": "Find the simple interest on ₹2,000 for 3 years at 5% per annum.",
                        "correct_answer": "₹300",
                        "explanation": "SI = (2000 × 3 × 5) / 100",
                        "is_demo": False,
                        "order": 1
                    },
                    {
                        "question": "What is the interest on ₹4,500 for 2 years at 6%?",
                        "correct_answer": "₹540",
                        "explanation": "SI = (4500 × 2 × 6) / 100",
                        "is_demo": False,
                        "order": 2
                    },
                    {
                        "question": "At 10% interest, how long will it take for ₹1,000 to earn ₹500 interest?",
                        "correct_answer": "5 years",
                        "explanation": "1000 × t × 10 /100 = 500 → t = 5",
                        "is_demo": False,
                        "order": 3
                    },
                    {
                        "question": "Find the principal if simple interest is ₹240 at 8% for 3 years.",
                        "correct_answer": "₹1,000",
                        "explanation": "Principal = SI × 100 / (R × T)",
                        "is_demo": False,
                        "order": 4
                    },
                    {
                        "question": "What is the total amount for ₹1,800 at 5% for 4 years?",
                        "correct_answer": "₹2,160",
                        "explanation": "SI = 1800 × 4 × 5 /100 = 360 → Amount = 1800 + 360",
                        "is_demo": False,
                        "order": 5
                    },
                ]
            },
            {
                "concept": "Ratio & Proportion",
                "questions": [
                    {
                        "question": "Divide ₹900 in the ratio 2:1.",
                        "correct_answer": "₹600 and ₹300",
                        "explanation": "Total 3 parts → 900×2/3 = 600, 900×1/3 = 300",
                        "is_demo": False,
                        "order": 1
                    },
                    {
                        "question": "Ratios 3:5 and 9:15 are?",
                        "correct_answer": "Equivalent",
                        "explanation": "3/5 = 9/15",
                        "is_demo": False,
                        "order": 2
                    },
                    {
                        "question": "If A:B = 4:7 and B:C = 3:5, find A:C.",
                        "correct_answer": "12:35",
                        "explanation": "Multiply: 4×3 : 7×5",
                        "is_demo": False,
                        "order": 3
                    },
                    {
                        "question": "A and B share money in ratio 5:4. If A gets ₹250, what is B’s share?",
                        "correct_answer": "₹200",
                        "explanation": "B = 250/5 × 4",
                        "is_demo": False,
                        "order": 4
                    },
                    {
                        "question": "If 8 workers take 15 days, how many days for 12 workers?",
                        "correct_answer": "10 days",
                        "explanation": "Inverse ratio → (8×15)/12 = 10",
                        "is_demo": False,
                        "order": 5
                    },
                ]
            },
            {
                "concept": "Ages",
                "questions": [
                    {
                        "question": "A is 6 years older than B. If A is 26, find B’s age.",
                        "correct_answer": "20 years",
                        "explanation": "26 − 6",
                        "is_demo": False,
                        "order": 1
                    },
                    {
                        "question": "Sum of ages of father and son is 50. Father is 32. Find son’s age.",
                        "correct_answer": "18 years",
                        "explanation": "50 − 32",
                        "is_demo": False,
                        "order": 2
                    },
                    {
                        "question": "Ratio of ages of A and B is 4:5. If B is 30, find A’s age.",
                        "correct_answer": "24 years",
                        "explanation": "A = 30×4/5",
                        "is_demo": False,
                        "order": 3
                    },
                    {
                        "question": "A is twice as old as B. If A is 28, find B’s age.",
                        "correct_answer": "14 years",
                        "explanation": "28/2",
                        "is_demo": False,
                        "order": 4
                    },
                    {
                        "question": "After 5 years, A will be 40. What is A’s present age?",
                        "correct_answer": "35 years",
                        "explanation": "40 − 5",
                        "is_demo": False,
                        "order": 5
                    },
                ]
            },
            {
                "concept": "Time & Work",
                "questions": [
                    {
                        "question": "A can finish a work in 10 days. How much work is done per day?",
                        "correct_answer": "1/10",
                        "explanation": "Work/day = 1 / days",
                        "is_demo": False,
                        "order": 1
                    },
                    {
                        "question": "A can do a job in 15 days, B in 10 days. How long together?",
                        "correct_answer": "6 days",
                        "explanation": "1/15 + 1/10 = 1/6",
                        "is_demo": False,
                        "order": 2
                    },
                    {
                        "question": "A alone does work in 8 days. After 2 days B joins. Total time?",
                        "correct_answer": "5 days",
                        "explanation": "A’s 2-day work + combined remaining work",
                        "is_demo": False,
                        "order": 3
                    },
                    {
                        "question": "12 men can finish a work in 6 days. How long for 9 men?",
                        "correct_answer": "8 days",
                        "explanation": "(12×6)/9 = 8",
                        "is_demo": False,
                        "order": 4
                    },
                    {
                        "question": "A completes work in 12 days, B in 8 days. What is efficiency ratio A:B?",
                        "correct_answer": "2:3",
                        "explanation": "Efficiency ∝ 1/time",
                        "is_demo": False,
                        "order": 5
                    },
                ]
            }
        ]

        # -----------------------------
        # Insert Into Database
        # -----------------------------

        for concept_data in data:
            concept_name = concept_data['concept']
            concept_obj, created = Concept.objects.get_or_create(name=concept_name)

            for q in concept_data['questions']:
                Question.objects.create(
                    concept=concept_obj,
                    question=q['question'],
                    explanation=q['explanation'],
                    correct_answer=q['correct_answer'],
                    is_demo=q['is_demo'],
                    order=q['order']
                )

        print("25 Questions Inserted Successfully!")
