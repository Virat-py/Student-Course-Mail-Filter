# Email Filter and Summarizer
## Problem

Students of IITD often receive a large volume of emails that may not be relevant to their specific courses or interests. This overwhelming influx of information can lead to important messages being overlooked. The email filter and summarizer aims to solve this problem by providing a tool that filters out irrelevant emails, allowing students to focus only on communications related to their enrolled courses.

## Overview

This project is a Python-based email filter and summarizer that connects to an IMAP email server, retrieves emails, filters them based on specific keywords, and summarizes their content using the Groq API. It is particularly useful for students and professionals looking to manage and synthesize important emails efficiently.


## Features

- **IMAP Email Retrieval**: Connects to an IMAP server to fetch emails from the inbox.
- **Keyword Filtering**: Filters emails based on defined keywords in both subject and body using re module.
- **Content Summarization**: Utilizes the Groq API to summarize email content in a concise manner.
- **Output Formatting**: Outputs the subject and summarized body of each relevant email.

## Technologies Used

- Python 3.x
- `imaplib`: For connecting to the email server.
- `email`: For handling email messages.
- `re`: For regular expression operations.
- `Groq`: For summarizing email content via an API.
