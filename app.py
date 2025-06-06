from flask import Flask, request, jsonify
from flask_cors import CORS
from interview_logic import generate_feedback
from dotenv import load_dotenv
import os
import traceback

# Load environment variables from .env file
load_dotenv()

# Read your API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("Loaded API key:", OPENROUTER_API_KEY)  # Remove or comment out in production

app = Flask(__name__)
CORS(app)

QUESTION_BANK = {
    "DSA": [
        "Explain how quicksort works and its average time complexity.",
        "Describe how a heap data structure is implemented and used.",
        "What are balanced binary trees? Explain AVL or Red-Black Trees.",
        "What is the difference between BFS and DFS?",
        "What is dynamic programming and how is it used?",
        "Explain Kadane’s algorithm.",
        "What are the applications of greedy algorithms?",
        "How do you detect a cycle in a directed graph?",
        "What is a Trie and where is it used?",
        "Explain union-find (disjoint set union).",
        "What is the time complexity of binary search?",
        "How do you implement LRU cache?",
        "What is backtracking? Give an example.",
        "What is memoization?",
        "Explain segment trees and their applications.",
        "How to detect and remove loop in a linked list?",
        "What are sliding window techniques?",
        "How to solve the N-Queens problem?",
        "How do you reverse a linked list?",
        "What is the longest common subsequence problem?",
        "How do you merge K sorted linked lists?",
        "What is the difference between stack and queue?",
        "Explain priority queues with heap.",
        "How to detect palindrome using two-pointer method?",
        "What is a monotonic stack?",
        "What is topological sorting?",
        "Explain graph coloring.",
        "What is a hash map and how is collision resolved?",
        "Explain Floyd-Warshall algorithm.",
        "Explain Dijkstra’s algorithm.",
        "What is the difference between recursion and iteration?",
        "What is a circular queue?",
        "What are bit manipulation techniques in DSA?",
        "What is the difference between array and linked list?",
        "How do you rotate an array?",
        "What is the difference between Min Heap and Max Heap?",
        "How to solve the subset sum problem?",
        "What is two pointer technique?",
        "Explain Rabin-Karp algorithm.",
        "What is the traveling salesman problem?"
    ],
    "ML": [
        "Explain bias-variance tradeoff and how to handle it.",
        "Describe the difference between supervised and unsupervised learning.",
        "What is regularization and why is it important?",
        "What are the types of cross-validation?",
        "What is overfitting and underfitting?",
        "What is the curse of dimensionality?",
        "Explain PCA (Principal Component Analysis).",
        "What are precision, recall, F1 score?",
        "What is logistic regression?",
        "Explain decision trees and pruning.",
        "What is a confusion matrix?",
        "What are support vector machines (SVM)?",
        "What is KNN (K-Nearest Neighbors)?",
        "Explain the working of Naive Bayes classifier.",
        "What are ensemble methods (e.g., Bagging, Boosting)?",
        "Explain gradient descent and variants.",
        "What is feature engineering?",
        "Explain how random forest works.",
        "What is XGBoost?",
        "What are learning curves?",
        "What is ROC-AUC curve?",
        "Explain clustering algorithms (e.g., K-Means).",
        "What is anomaly detection?",
        "What are hyperparameters and how do you tune them?",
        "What is grid search and random search?",
        "What is a cost function?",
        "What is early stopping in ML?",
        "Explain time series forecasting.",
        "What is reinforcement learning?",
        "What is the difference between batch and online learning?",
        "What are activation functions in neural networks?",
        "What is dropout in deep learning?",
        "What is transfer learning?",
        "What is the vanishing gradient problem?",
        "What is an epoch in ML?",
        "What is A/B testing?",
        "What is the difference between generative and discriminative models?",
        "What is the bag-of-words model?",
        "Explain word embeddings (Word2Vec, GloVe).",
        "What are CNNs and RNNs?"
    ],
    "Web Developer": [
        "Explain the event loop in JavaScript.",
        "What are closures and how are they used?",
        "Describe RESTful APIs and HTTP methods.",
        "What is the difference between GET and POST?",
        "What are promises and async/await?",
        "What is hoisting in JavaScript?",
        "Explain the DOM and its manipulation.",
        "What is the difference between == and ===?",
        "What are cookies, sessionStorage and localStorage?",
        "What is CORS and how is it handled?",
        "What is the virtual DOM in React?",
        "What are props and state in React?",
        "Explain the lifecycle methods in React.",
        "What is useEffect hook in React?",
        "What is responsive web design?",
        "What is the box model in CSS?",
        "What are CSS flexbox and grid?",
        "What is the difference between class and id in HTML/CSS?",
        "What are HTML semantic tags?",
        "What are SPA and MPA?",
        "What is Webpack and why is it used?",
        "What is Babel in frontend development?",
        "Explain MVC architecture.",
        "How does authentication work in web apps?",
        "What are JWT tokens?",
        "What is OAuth?",
        "Explain SSR and CSR in web applications.",
        "What is a Service Worker?",
        "What is Progressive Web App (PWA)?",
        "Explain HTTPS and SSL.",
        "What is a 404 and 500 error?",
        "What are CRUD operations?",
        "What is event bubbling and event delegation?",
        "What is memoization in React?",
        "What is a Higher-Order Component (HOC)?",
        "How does routing work in React (React Router)?",
        "What is context API?",
        "What are controlled and uncontrolled components?",
        "What are custom hooks?",
        "What is Redux and when to use it?"
    ],
    "DBMS": [
        "What is normalization? Explain types.",
        "What are ACID properties?",
        "Difference between primary key and unique key?",
        "Explain different types of JOINs.",
        "What is indexing and why is it important?",
        "What is a view?",
        "What is a trigger in SQL?",
        "Explain transactions in DBMS.",
        "What is a foreign key?",
        "What is the difference between DELETE and TRUNCATE?",
        "What are stored procedures?",
        "What is SQL injection?",
        "Explain ER model with example.",
        "What is a subquery?",
        "What is a schema?",
        "Explain 1NF, 2NF, 3NF with examples.",
        "What is denormalization?",
        "What is a clustered index vs non-clustered index?",
        "What is the difference between RDBMS and NoSQL?",
        "What is the difference between SQL and PL/SQL?",
        "What is a deadlock in DBMS?",
        "What are phantom reads?",
        "Explain concurrency control in DBMS.",
        "What is a lock and types of locks?",
        "Explain two-phase commit protocol.",
        "What is RAID in storage?",
        "What is a checkpoint in DBMS?",
        "What is the difference between having and where clause?",
        "What are aggregate functions in SQL?",
        "What is a self join?",
        "What is an alias in SQL?",
        "What is the use of GROUP BY clause?",
        "Explain UNION vs UNION ALL.",
        "What is a Cartesian product in SQL?",
        "What are integrity constraints?",
        "What is a correlated subquery?",
        "How does indexing improve query performance?",
        "What is hashing in DBMS?",
        "Explain file organization techniques in DBMS.",
        "What are multivalued dependencies?"
    ],
    "CN": [
        "What is the OSI model? Explain each layer.",
        "What is the TCP/IP model?",
        "Difference between TCP and UDP.",
        "What is IP address and types?",
        "What is DNS and how does it work?",
        "What is subnetting?",
        "What is ARP protocol?",
        "What is ICMP?",
        "What is a router vs switch?",
        "What is NAT (Network Address Translation)?",
        "What is DHCP?",
        "What is HTTP and HTTPS?",
        "Explain 3-way handshake in TCP.",
        "What is congestion control?",
        "What is flow control?",
        "What are firewalls and how do they work?",
        "What is packet switching vs circuit switching?",
        "Explain MAC addressing.",
        "What is CSMA/CD?",
        "What is port forwarding?",
        "Explain SSL/TLS.",
        "What is a VPN?",
        "What is ping and traceroute?",
        "What are sockets in networking?",
        "What is bandwidth vs latency?",
        "What is a proxy server?",
        "Explain QoS in networking.",
        "What is a VLAN?",
        "What is tunneling?",
        "What is a load balancer?",
        "What is the purpose of headers in packets?",
        "What are well-known ports?",
        "What is SMTP, POP3, IMAP?",
        "What is network topology?",
        "What is multicast vs broadcast?",
        "What is BGP?",
        "What is DNS poisoning?",
        "What is packet sniffing?",
        "What are IPv4 and IPv6 differences?",
        "What is MTU?"
    ],
    "OS": [
        "What is a process and thread?",
        "What is a deadlock and how to prevent it?",
        "Explain process scheduling algorithms.",
        "What is context switching?",
        "What are system calls?",
        "Explain inter-process communication (IPC).",
        "What is a semaphore?",
        "What is a race condition?",
        "Explain paging and segmentation.",
        "What is virtual memory?",
        "What is demand paging?",
        "What is thrashing?",
        "What is the difference between process and program?",
        "Explain the states of a process.",
        "What is multithreading?",
        "What is the difference between user and kernel mode?",
        "What is priority inversion?",
        "What are page replacement algorithms?",
        "What is memory fragmentation?",
        "What is a file system?",
        "Explain inode structure.",
        "What is a bootloader?",
        "What is swapping?",
        "What is the difference between preemptive and non-preemptive scheduling?",
        "What is time-sharing OS?",
        "What is an interrupt?",
        "Explain first-come-first-serve (FCFS).",
        "Explain round robin scheduling.",
        "What is mutual exclusion?",
        "What are orphan and zombie processes?",
        "What is the difference between fork() and exec()?",
        "What is a shell in OS?",
        "What is kernel panic?",
        "What is cron job?",
        "What is memory-mapped I/O?",
        "What are system daemons?",
        "What is device driver?",
        "What is caching in OS?",
        "Explain producer-consumer problem."
    ],
    "System Design": [
       "What is system design? Why is it important?",
        "How do you design a URL shortening service like bit.ly?",
        "Design a scalable chat application.",
        "How would you design Twitter/Reddit?",
        "Design a system like Uber or Ola.",
        "What is load balancing and how would you implement it?",
        "What is sharding in databases?",
        "What is a CDN? How does it help scalability?",
        "How would you design a video streaming service like YouTube?",
        "What is the difference between horizontal and vertical scaling?",
        "Explain CAP theorem.",
        "What is eventual consistency?",
        "How do you handle database replication?",
        "How to design a web crawler?",
        "Design a notification system (e.g., push/email alerts).",
        "What is caching? Where should you use it?",
        "How would you design a rate limiter?",
        "How would you scale a database?",
        "Design an API rate-limiting system.",
        "How would you handle failover in a distributed system?",
        "What is the role of message queues in system design?",
        "What is a microservice architecture?",
        "Design a news feed system like Facebook.",
        "How would you implement file storage (like Dropbox)?",
        "Design a real-time collaboration system (like Google Docs).",
        "Explain master-slave vs multi-master architecture.",
        "What is data partitioning and how is it done?",
        "What are some common system design bottlenecks?",
        "How would you design an e-commerce website?",
        "Design a search autocomplete feature.",
        "What is a reverse proxy?",
        "How would you monitor a large-scale system?",
        "Explain the use of Redis in system design.",
        "How to design a log aggregation system?",
        "How to store and serve large images efficiently?",
        "How would you ensure high availability in a system?",
        "Explain distributed hashing and consistent hashing.",
        "What is a heartbeat mechanism in distributed systems?",
        "How to prevent data loss in a large-scale system?",
        "What are the key metrics to monitor in a scalable system?"
    ],
    "DevOps": [
         "What is DevOps and why is it important?",
        "What are the key components of a CI/CD pipeline?",
        "Explain the difference between continuous integration, delivery, and deployment.",
        "What is Infrastructure as Code (IaC)?",
        "What are popular CI/CD tools? (e.g., Jenkins, GitLab CI)",
        "What is Docker? How is it used in DevOps?",
        "Explain the concept of containers vs virtual machines.",
        "What is Kubernetes and how does it work?",
        "What are Helm charts?",
        "What is version control? Explain Git branching strategy.",
        "What is monitoring and logging in DevOps?",
        "What is Prometheus and Grafana used for?",
        "Explain the 12-factor app methodology.",
        "What is blue-green deployment?",
        "What is canary deployment?",
        "What are artifacts and artifact repositories?",
        "What is the purpose of Ansible/Chef/Puppet?",
        "What are some best practices for DevOps?",
        "What is the difference between monoliths and microservices?",
        "Explain load testing and stress testing.",
        "How do you handle rollback in production?",
        "What is Jenkins pipeline? Example?",
        "What is GitOps?",
        "What is a build tool? Examples (Maven, Gradle)?",
        "How do you secure a CI/CD pipeline?",
        "What is container orchestration?",
        "What are stateful and stateless applications?",
        "How do you manage secrets in DevOps?",
        "Explain the concept of service discovery.",
        "What are feature flags?",
        "What is a reverse proxy in DevOps context?",
        "How do you implement disaster recovery?",
        "What is the difference between Docker image and container?",
        "What is a rolling update?",
        "What is the difference between Jenkins freestyle and pipeline project?",
        "How do you monitor microservices?",
        "What is Site Reliability Engineering (SRE)?",
        "Explain the use of Terraform.",
        "What are logs aggregation tools? (ELK stack)",
        "What is the difference between continuous testing and traditional testing?"
    ]
}

user_progress = {}

@app.route('/get_question', methods=['POST'])
def get_question():
    data = request.get_json()
    role = data.get('role')
    session_id = data.get('session_id')

    if not role or not session_id:
        return jsonify({"error": "Missing 'role' or 'session_id'"}), 400

    if role not in QUESTION_BANK:
        return jsonify({"question": "No questions available for this role."})

    if session_id not in user_progress:
        user_progress[session_id] = {}

    idx = user_progress[session_id].get(role, 0)
    questions = QUESTION_BANK[role]

    if idx >= len(questions):
        return jsonify({"question": "You have completed all questions for this role. Congratulations!"})

    question = questions[idx]
    return jsonify({"question": question})

@app.route('/try_again', methods=['POST'])
def try_again():
    data = request.get_json()
    role = data.get('role')
    session_id = data.get('session_id')

    if not role or not session_id:
        return jsonify({"error": "Missing 'role' or 'session_id'"}), 400

    if session_id in user_progress and role in user_progress[session_id]:
        idx = user_progress[session_id][role]
        question = QUESTION_BANK[role][idx]
        return jsonify({"question": question})

    return jsonify({"question": "No active question found, please request a new question."}), 404

@app.route('/next_question', methods=['POST'])
def next_question():
    data = request.get_json()
    role = data.get('role')
    session_id = data.get('session_id')

    if not role or not session_id:
        return jsonify({"error": "Missing 'role' or 'session_id'"}), 400

    if session_id not in user_progress:
        user_progress[session_id] = {}

    idx = user_progress[session_id].get(role, 0) + 1
    questions = QUESTION_BANK.get(role, [])

    if idx >= len(questions):
        return jsonify({"question": "You have completed all questions for this role. Great job!"})

    user_progress[session_id][role] = idx
    question = questions[idx]
    return jsonify({"question": question})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        role = data.get('role')
        answer = data.get('answer')

        print("DEBUG: role =", role)
        print("DEBUG: answer =", answer)

        feedback = generate_feedback(role, answer)
        return jsonify({'feedback': feedback})
    except Exception as e:
        print("ERROR in /ask:")
        traceback.print_exc()
        return jsonify({'feedback': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
