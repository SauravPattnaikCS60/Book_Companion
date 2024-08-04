chapter_to_title_mappers = {
    "Programming Python": {
        "1": "A Sneak Preview",
        "2": "System Tools",
        "3": "Script Execution Context",
        "4": "File and Directory Tools",
        "5": "Parallel System Tools",
        "6": "Complete System Programs",
        "7": "Graphical User Interfaces",
        "8": "A tkinter Tour, Part 1",
        "9": "A tkinter Tour, Part 2",
        "10": "GUI Coding Techniques",
        "11": "Complete GUI Programs",
        "12": "Network Scripting",
        "13": "Client-Side Scripting",
        "14": "The PyMailGUI Client",
        "15": "Server-Side Scripting",
        "16": "The PyMailCGI Server",
        "17": "Databases and Persistence",
        "18": "Data Structures",
        "19": "Text and Language",
        "20": "Python C Integration",
    },
    "Vikings": {
        "1": "The Vikings",
        "2": "Traders and Raiders",
        "3": "Viking Sailors and Ships",
        "4": "Eric the Red",
        "5": "Leif Eriksson",
        "6": "Viking Gods and Myths",
    },
    "Introduction to ML": {
        "1": "Preliminaries",
        "2": "Boolean Functions",
        "3": "Using Version Spaces for Learning",
        "4": "Neural Networks",
        "5": "Statistical Learning",
        "6": "Decision Trees",
        "7": "Inductive Logic Programming",
        "8": "Computational Learning Theory",
        "9": "Unsupervised Learning",
        "10": "Temporal-Difference Learning",
        "11": "Delayed-Reinforcement Learning",
        "12": "Explanation-Based Learning",
    },
}
book_file_mapping = {
    "Programming Python": "book1.pdf",
    "Vikings": "book2.pdf",
    "Introduction to ML": "book3.pdf",
    "A Short History of Nearly Everything": "book4.pdf",
}
chapter_numbers_mapper = {
    "Programming Python": tuple([f"CHAPTER {number}" for number in range(1, 21)]),
    "Vikings": tuple([f"Chapter {number}" for number in range(1, 7)]),
    "Introduction to ML": tuple([f"Chapter {number}" for number in range(1, 13)]),
}

base_path = 'data/'