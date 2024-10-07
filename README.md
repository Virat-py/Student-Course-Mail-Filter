# Email Filter and Summarizer

you can access the working project here: https://student-course-mail-filter-dhyrxa8guefnzqs2ivpqbf.streamlit.app/
<img width="1469" alt="Screenshot 2024-10-06 at 3 56 18 PM" src="https://github.com/user-attachments/assets/351db932-4fb0-48c8-955d-c7dc7869d30e">

## Problem

Students of IITD often receive a large volume of emails that may not be relevant to their specific courses or interests. This overwhelming influx of information can lead to important messages being overlooked. The email filter and summarizer aims to solve this problem by providing a tool that filters out irrelevant emails, allowing students to focus only on communications related to their enrolled courses.

## Overview

This project is a Python-based Email Filter and Summarizer that connects to an IMAP email server, retrieves emails, filters them based on specific keywords, and presents their content using a Streamlit interface. It is particularly useful for students and professionals looking to manage and synthesize important emails efficiently.

## Features

- **IMAP Email Retrieval**: Connects to an IMAP server to fetch emails from the inbox.
- **Keyword Filtering**: Filters emails based on defined keywords in both subject and body using re module.
- **Streamlit Interface**: Provides an interactive web application for users to log in and view relevant emails seamlessly.

## Technologies Used

- Python 3.x
- `imaplib`: For connecting to the email server.
- `email`: For handling email messages.
- `re`: For regular expression operations.
- `Streamlit`: For creating the user interface.
