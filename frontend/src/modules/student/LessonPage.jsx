

// import React, { useState, useEffect, useRef } from 'react';
// import { useParams, useNavigate } from 'react-router-dom';
// import { 
//   ArrowLeft, 
//   CheckCircle, 
//   FileText, 
//   MessageCircle, 
//   Clock, 
//   Lock, 
//   ChevronRight,
//   X,
//   AlertCircle,
//   Play
// } from 'lucide-react';

// const LessonPage = () => {
//   const { class: classNumber, subject, chapterNumber } = useParams();
//   const navigate = useNavigate();
//   const [currentTime, setCurrentTime] = useState(0);
//   const videoRef = useRef(null);
//   const [isVideoCompleted, setIsVideoCompleted] = useState(false);
//   const [showPdf, setShowPdf] = useState(false);
//   const [showQuiz, setShowQuiz] = useState(false);
//   const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
//   const [selectedAnswer, setSelectedAnswer] = useState(null);
//   const [quizScore, setQuizScore] = useState(0);
//   const [quizCompleted, setQuizCompleted] = useState(false);
//   const [remainingChances, setRemainingChances] = useState(3);
  
//   // Centralized state for the checklist
//   const [checklistStatus, setChecklistStatus] = useState({
//     videoWatched: false,
//     practiceAttempted: false,
//     quizPassed: false
//   });

//   // Sample quiz questions for each class, subject and chapter
//   const quizQuestions = {
//     '7': {
//       Maths: {
//         1: [
//           {
//             question: "What is the place value of 7 in the number 3,74,581?",
//             options: ["Thousands", "Ten Thousands", "Hundred Thousands", "Ones"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which of these is the largest number?",
//             options: ["99,999", "1,00,000", "9,999", "99,99,999"],
//             correctAnswer: 3
//           },
//           {
//             question: "How do you write five lakh twenty thousand in numerals?",
//             options: ["5,20,000", "5,02,000", "5,00,200", "50,20,000"],
//             correctAnswer: 0
//           }
//         ],
//         2: [
//           {
//             question: "What is the result of 15 + 7 × 3?",
//             options: ["66", "36", "44", "56"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which operation should be performed first in the expression: 8 + (12 ÷ 4) × 2?",
//             options: ["Addition", "Multiplication", "Division", "Subtraction"],
//             correctAnswer: 2
//           },
//           {
//             question: "What is the value of 20 - (5 × 2) + 3?",
//             options: ["13", "17", "23", "33"],
//             correctAnswer: 0
//           }
//         ],
//         3: [
//           {
//             question: "What is a point in geometry?",
//             options: ["A location with no size", "A straight path", "A flat surface", "A line with two endpoints"],
//             correctAnswer: 0
//           },
//           {
//             question: "What is a ray?",
//             options: ["A line with two endpoints", "A part of a line with one endpoint", "A curved path", "A flat surface"],
//             correctAnswer: 1
//           },
//           {
//             question: "How many dimensions does a point have?",
//             options: ["Zero", "One", "Two", "Three"],
//             correctAnswer: 0
//           }
//         ],
//         4: [
//           {
//             question: "What is the value of x in the expression 2x + 5 = 15?",
//             options: ["5", "10", "7.5", "5.5"],
//             correctAnswer: 0
//           },
//           {
//             question: "Solve for y: 3y - 2 = 10.",
//             options: ["2", "3", "4", "5"],
//             correctAnswer: 2
//           },
//           {
//             question: "If a + 7 = 13, what is the value of a?",
//             options: ["4", "5", "6", "7"],
//             correctAnswer: 2
//           }
//         ],
//         5: [
//           {
//             question: "How many endpoints does a line have?",
//             options: ["0", "1", "2", "Infinite"],
//             correctAnswer: 0
//           },
//           {
//             question: "A line segment is part of a:",
//             options: ["Ray", "Point", "Line", "Plane"],
//             correctAnswer: 2
//           },
//           {
//             question: "Which of these extends infinitely in only one direction?",
//             options: ["Line", "Ray", "Line Segment", "Point"],
//             correctAnswer: 1
//           }
//         ]
//       },
//       Science: {
//         1: [
//           {
//             question: "Which century is known as the 'Age of Science'?",
//             options: ["18th Century", "19th Century", "20th Century", "21st Century"],
//             correctAnswer: 2
//           },
//           {
//             question: "Who is known as the father of modern science?",
//             options: ["Albert Einstein", "Galileo Galilei", "Isaac Newton", "Marie Curie"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which invention revolutionized communication in the 20th century?",
//             options: ["Telephone", "Internet", "Printing Press", "Television"],
//             correctAnswer: 1
//           }
//         ],
//         2: [
//           {
//             question: "Which of these is a chemical property?",
//             options: ["Color", "Flammability", "Density", "Hardness"],
//             correctAnswer: 1
//           },
//           {
//             question: "What is the state of matter where particles are tightly packed and vibrate in fixed positions?",
//             options: ["Liquid", "Gas", "Solid", "Plasma"],
//             correctAnswer: 2
//           },
//           {
//             question: "The process by which a solid changes directly into a gas is called:",
//             options: ["Melting", "Evaporation", "Sublimation", "Condensation"],
//             correctAnswer: 2
//           }
//         ],
//         3: [
//           {
//             question: "What is the unit of electric current?",
//             options: ["Volt", "Ampere", "Ohm", "Watt"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which component is used to break or make an electric circuit?",
//             options: ["Battery", "Wire", "Switch", "Bulb"],
//             correctAnswer: 2
//           },
//           {
//             question: "What is the flow of electric charge called?",
//             options: ["Voltage", "Resistance", "Current", "Power"],
//             correctAnswer: 2
//           }
//         ],
//         4: [
//           {
//             question: "Which metal is liquid at room temperature?",
//             options: ["Iron", "Mercury", "Gold", "Copper"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which of these is a good conductor of electricity?",
//             options: ["Wood", "Plastic", "Copper", "Rubber"],
//             correctAnswer: 2
//           },
//           {
//             question: "What property makes metals suitable for making bells?",
//             options: ["Ductility", "Malleability", "Sonorousness", "Lustre"],
//             correctAnswer: 2
//           }
//         ],
//         5: [
//           {
//             question: "Which of these is a chemical change?",
//             options: ["Melting ice", "Dissolving sugar", "Burning wood", "Breaking glass"],
//             correctAnswer: 2
//           },
//           {
//             question: "In a physical change, what changes?",
//             options: ["Chemical composition", "State or appearance", "Both chemical composition and state", "Nothing"],
//             correctAnswer: 1
//           },
//           {
//             question: "Rusting of iron is an example of a:",
//             options: ["Physical change", "Chemical change", "Reversible change", "No change"],
//             correctAnswer: 1
//           }
//         ]
//       },
//       Social: {
//         1: [
//           {
//             question: "What period does 'A Thousand Years' refer to in Indian history?",
//             options: ["700-1700 CE", "500-1500 CE", "1000-2000 CE", "800-1800 CE"],
//             correctAnswer: 0
//           },
//           {
//             question: "Which language was predominantly used for administrative purposes during the Delhi Sultanate?",
//             options: ["Sanskrit", "Persian", "Arabic", "Urdu"],
//             correctAnswer: 1
//           },
//           {
//             question: "What was the main source of information about the past for historians?",
//             options: ["Coins", "Inscriptions", "Manuscripts", "All of the above"],
//             correctAnswer: 3
//           }
//         ],
//         2: [
//           {
//             question: "Which was the first major kingdom in South India?",
//             options: ["Chola", "Pandya", "Chera", "Satavahana"],
//             correctAnswer: 3
//           },
//           {
//             question: "Who was a prominent ruler of the Chola dynasty?",
//             options: ["Rajendra Chola I", "Ashoka", "Harsha", "Chandragupta Maurya"],
//             correctAnswer: 0
//           },
//           {
//             question: "The Rashtrakutas were known for their contributions to:",
//             options: ["Art and Architecture", "Trade Routes", "Military Strategy", "Farming Techniques"],
//             correctAnswer: 0
//           }
//         ],
//         3: [
//           {
//             question: "Who was the first Sultan of Delhi?",
//             options: ["Iltutmish", "Qutb-ud-din Aibak", "Balban", "Alauddin Khilji"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which monument was built by Qutb-ud-din Aibak?",
//             options: ["Red Fort", "Qutb Minar", "Humayun's Tomb", "Agra Fort"],
//             correctAnswer: 1
//           },
//           {
//             question: "Raziya Sultan was the daughter of which Sultan?",
//             options: ["Ghiyas ud din Balban", "Iltutmish", "Nasir ud din Mahmud", "Alauddin Khalji"],
//             correctAnswer: 1
//           }
//         ],
//         4: [
//           {
//             question: "Who was the first Mughal emperor?",
//             options: ["Akbar", "Babur", "Humayun", "Jahangir"],
//             correctAnswer: 1
//           },
//           {
//             question: "The Battle of Panipat (1526) was fought between Babur and:",
//             options: ["Sher Shah Suri", "Ibrahim Lodi", "Hem Chandra Vikramaditya", "Rana Sanga"],
//             correctAnswer: 1
//           },
//           {
//             question: "Akbar's revenue minister was:",
//             options: ["Birbal", "Faizi", "Raja Todar Mal", "Tansen"],
//             correctAnswer: 2
//           }
//         ],
//         5: [
//           {
//             question: "Which ruler built the Taj Mahal?",
//             options: ["Akbar", "Shah Jahan", "Aurangzeb", "Jahangir"],
//             correctAnswer: 1
//           },
//           {
//             question: "The Red Fort in Delhi was built by:",
//             options: ["Humayun", "Akbar", "Shah Jahan", "Aurangzeb"],
//             correctAnswer: 2
//           },
//           {
//             question: "The Qutb Minar was started by Qutb-ud-din Aibak and completed by:",
//             options: ["Firoz Shah Tughlaq", "Iltutmish", "Alauddin Khalji", "Ghiyas ud din Balban"],
//             correctAnswer: 1
//           }
//         ]
//       },
//       English: {
//         1: [
//           {
//             question: "Which of the following is a common noun?",
//             options: ["Table", "London", "John", "Amazon"],
//             correctAnswer: 0
//           },
//           {
//             question: "Identify the verb in the sentence: 'She sings beautifully.'",
//             options: ["She", "sings", "beautifully", "the"],
//             correctAnswer: 1
//           },
//           {
//             question: "A proper noun always begins with a:",
//             options: ["Lowercase letter", "Uppercase letter", "Vowel", "Consonant"],
//             correctAnswer: 1
//           }
//         ],
//         2: [
//           {
//             question: "What is a synonym for 'happy'?",
//             options: ["Sad", "Joyful", "Angry", "Tired"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which of these is an antonym for 'fast'?",
//             options: ["Quick", "Rapid", "Slow", "Speedy"],
//             correctAnswer: 2
//           },
//           {
//             question: "The word 'tiny' is a synonym for:",
//             options: ["Large", "Huge", "Small", "Giant"],
//             correctAnswer: 2
//           }
//         ],
//         3: [
//           {
//             question: "Which of the following is a preposition?",
//             options: ["Run", "Quickly", "Under", "And"],
//             correctAnswer: 2
//           },
//           {
//             question: "In the sentence 'The cat sat on the mat,' what is the adjective?",
//             options: ["Cat", "Sat", "On", "None of the above"],
//             correctAnswer: 3
//           },
//           {
//             question: "An adverb usually describes a:",
//             options: ["Noun", "Verb", "Pronoun", "Preposition"],
//             correctAnswer: 1
//           }
//         ],
//         4: [
//           {
//             question: "What is the past tense of the verb 'go'?",
//             options: ["Goes", "Gone", "Went", "Going"],
//             correctAnswer: 2
//           },
//           {
//             question: "Which of these is a collective noun?",
//             options: ["Book", "Tree", "Flock", "Car"],
//             correctAnswer: 2
//           },
//           {
//             question: "A sentence that expresses a strong emotion is called an:",
//             options: ["Interrogative sentence", "Imperative sentence", "Exclamatory sentence", "Declarative sentence"],
//             correctAnswer: 2
//           }
//         ],
//         5: [
//           {
//             question: "What punctuation mark is used at the end of a question?",
//             options: ["Period", "Comma", "Question mark", "Exclamation mark"],
//             correctAnswer: 2
//           },
//           {
//             question: "Which of these is a conjunction?",
//             options: ["Jump", "But", "Loudly", "Beautiful"],
//             correctAnswer: 1
//           },
//           {
//             question: "The subject of a sentence is usually a:",
//             options: ["Verb or Adverb", "Noun or Pronoun", "Adjective or Preposition", "Conjunction or Interjection"],
//             correctAnswer: 1
//           }
//         ]
//       },
//       Computer: {
//         1: [
//           {
//             question: "What does CPU stand for?",
//             options: ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Power Unit"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which of these is an input device?",
//             options: ["Monitor", "Printer", "Keyboard", "Speaker"],
//             correctAnswer: 2
//           },
//           {
//             question: "The brain of the computer is the:",
//             options: ["Monitor", "Keyboard", "Mouse", "CPU"],
//             correctAnswer: 3
//           }
//         ],
//         2: [
//           {
//             question: "What is RAM primarily used for in a computer?",
//             options: ["Long-term storage", "Temporary data storage", "Printing documents", "Displaying images"],
//             correctAnswer: 1
//           },
//           {
//             question: "Which operating system is developed by Microsoft?",
//             options: ["macOS", "Linux", "Windows", "Android"],
//             correctAnswer: 2
//           },
//           {
//             question: "An operating system is a type of:",
//             options: ["Hardware", "Application Software", "System Software", "Utility Software"],
//             correctAnswer: 2
//           }
//         ],
//         3: [
//           {
//             question: "What is the full form of WWW?",
//             options: ["World Wide Web", "World Web Windows", "Web World Wide", "Wide World Web"],
//             correctAnswer: 0
//           },
//           {
//             question: "Which protocol is used to send emails?",
//             options: ["HTTP", "FTP", "SMTP", "TCP/IP"],
//             correctAnswer: 2
//           },
//           {
//             question: "A collection of interconnected networks is known as the:",
//             options: ["Intranet", "Extranet", "Internet", "LAN"],
//             correctAnswer: 2
//           }
//         ],
//         4: [
//           {
//             question: "Which software is used for creating documents, spreadsheets, and presentations?",
//             options: ["Antivirus", "Operating System", "Office Suite", "Web Browser"],
//             correctAnswer: 2
//           },
//           {
//             question: "What is a 'bug' in computer programming?",
//             options: ["A computer virus", "An error in the code", "A type of software", "A hardware component"],
//             correctAnswer: 1
//           },
//           {
//             question: "Compilers and interpreters are examples of:",
//             options: ["Application software", "System software", "Utility programs", "Hardware"],
//             correctAnswer: 1
//           }
//         ],
//         5: [
//           {
//             question: "What does 'HTTP' stand for?",
//             options: ["HyperText Transfer Protocol", "Hyper Transfer Text Protocol", "High Technology Transfer Program", "Home Text Transfer Protocol"],
//             correctAnswer: 0
//           },
//           {
//             question: "Which device is used to connect multiple computers in a local area network (LAN)?",
//             options: ["Modem", "Router", "Switch", "Server"],
//             correctAnswer: 2
//           },
//           {
//             question: "What is cybersecurity primarily concerned with?",
//             options: ["Making computers faster", "Protecting computer systems from theft and damage", "Designing new computer hardware", "Creating software applications"],
//             correctAnswer: 1
//           }
//         ]
//       }
//     },
//     '8': {
//       // Add quiz questions for Class 8 subjects here
//       Maths: {
//         1: [
//           {
//             question: "What is a rational number?",
//             options: ["A number that can be expressed as a fraction", "A whole number", "An irrational number", "A prime number"],
//             correctAnswer: 0
//           },
//           {
//             question: "Which of these is a rational number?",
//             options: ["π", "√2", "0.75", "e"],
//             correctAnswer: 2
//           },
//           {
//             question: "What is the additive inverse of 3/4?",
//             options: ["4/3", "-3/4", "-4/3", "3/4"],
//             correctAnswer: 1
//           }
//         ],
//         // Add more chapters for Class 8 Maths
//       },
//       Science: {
//         1: [
//           {
//             question: "What is crop production?",
//             options: ["Growing plants for food", "Manufacturing crops", "Processing agricultural products", "Selling crops"],
//             correctAnswer: 0
//           },
//           {
//             question: "Which of these is a kharif crop?",
//             options: ["Wheat", "Rice", "Barley", "Mustard"],
//             correctAnswer: 1
//           },
//           {
//             question: "What is the process of loosening and turning of soil called?",
//             options: ["Harvesting", "Irrigation", "Tilling", "Sowing"],
//             correctAnswer: 2
//           }
//         ],
//         // Add more chapters for Class 8 Science
//       },
//       // Add other subjects for Class 8
//     },
//     '9': {
//       // Add quiz questions for Class 9 subjects here
//     },
//     '10': {
//       // Add quiz questions for Class 10 subjects here
//     }
//   };

//   // Generate unique key for each chapter's quiz chances
//   const getChapterKey = () => `quiz_chances_${classNumber}_${subject}_${chapterNumber}`;
//   const getChapterDateKey = () => `quiz_date_${classNumber}_${subject}_${chapterNumber}`;

//   useEffect(() => {
//     const today = new Date().toDateString();
//     const chapterKey = getChapterKey();
//     const chapterDateKey = getChapterDateKey();
    
//     const storedDate = localStorage.getItem(chapterDateKey);
//     const storedChances = localStorage.getItem(chapterKey);
    
//     if (storedDate === today) {
//       // Same day, use stored chances for this chapter
//       setRemainingChances(parseInt(storedChances) || 3);
//     } else {
//       // New day, reset chances for this chapter
//       setRemainingChances(3);
//       localStorage.setItem(chapterKey, '3');
//       localStorage.setItem(chapterDateKey, today);
//     }
//   }, [classNumber, subject, chapterNumber]);

//   // Update checklist when video is completed
//   useEffect(() => {
//     if (isVideoCompleted) {
//       setChecklistStatus(prev => ({
//         ...prev,
//         videoWatched: true
//       }));
//     }
//   }, [isVideoCompleted]);

//   const videos = {
//     '7': {
//       Maths: {
//       1: { title: "Large Numbers", file: "/videos/Maths/chapter-1.mp4", pdf: "/pdfs/maths/maths ch-1.pdf", about: "Learn about large numbers, their place values, and representation." },
//       2: { title: "Arithmetic Expressions", file: "/videos/Maths/chapter-2.mp4", pdf: "/pdfs/maths/maths ch-2.pdf", about: "Understand arithmetic expressions and step-by-step solving." },
//       3: { title: "Peek Point", file: "/videos/Maths/chapter-3.mp4", pdf: "/pdfs/maths/maths ch-3.pdf", about: "Explore fundamental geometry concepts like points, lines, and rays." },
//       4: { title: "Number Expressions", file: "/videos/Maths/chapter-4.mp4", pdf: "/pdfs/maths/maths ch-4.pdf", about: "Dive into solving simple algebraic equations with one variable." },
//       5: { title: "Lines and Angles", file: "/videos/Maths/chapter-5.mp4", pdf: "/pdfs/maths/maths ch-5.pdf", about: "Introduction to lines, line segments, rays, and basic angles." },
//     },
//     Science: {
//       1: { title: "Age of Science", file: "/videos/science/chapter-1.mp4", pdf: "/pdfs/science/7-Science-chpt-1.pdf", about: "Discover the role of science in human progress and historical context." },
//       2: { title: "Substances", file: "/videos/science/chapter-2.mp4", pdf: "/pdfs/science/7-Science-chpt-2.pdf", about: "Learn about different states of matter and their properties." },
//       3: { title: "Electricity Basics", file: "/videos/science/chapter-3.mp4", pdf: "/pdfs/science/7-Science-chpt-3.pdf", about: "Basics of electricity, current, circuits, and components." },
//       4: { title: "Metals & Non-metals", file: "/videos/science/chapter-4.mp4", pdf: "/pdfs/science/7-Science-chpt-4.pdf", about: "Study the properties, uses, and differences between metals and non-metals." },
//       5: { title: "Physical & Chemical Changes", file: "/videos/science/chapter-5.mp4", pdf: "/pdfs/science/7-Science-chpt-5.pdf", about: "Differentiate physical changes from chemical changes with examples." },
//     },
//     Social: {
//       1: { title: "Tracing Changes", file: "/videos/social/chapter1 (online-video-cutter.com).mp4", pdf: "/pdfs/social/History (1)Tracing Changes Through A Thousand Years.pdf", about: "Explore historical changes and sources over a thousand years in India." },
//       2: { title: "New Kings & Kingdoms", file: "/videos/social/chpter2social.mp4", pdf: "/pdfs/social/History (2)New Kings And Kingdoms.pdf", about: "Learn about the rise of various kingdoms in medieval India." },
//       3: { title: "The Delhi Sultans", file: "/videos/social/social_ch3.mp4.mp4", pdf: "/pdfs/social/History (3)The Delhi Sultans.pdf", about: "Know about the Delhi Sultans, their administration, and monuments." },
//       4: { title: "The Mughal Empire", file: "/videos/social/social_ch4.mp4.mp4", pdf: "/pdfs/social/History (4)The Mughal Empire.pdf", about: "A detailed look into the Mughal Empire, its rulers, and policies." },
//       5: { title: "Rulers and Buildings", file: "/videos/social/social_ch5.mp4.mp4", pdf: "/pdfs/social/History (5)Rulers and Buildings.pdf", about: "Study the architectural marvels and ruling strategies of various historical rulers." },
//     },
//     English: {
//       1: { title: "Learning Together", file: "/videos/english/7th english unit -1 LEARNING TOGETHER (2).mp4", pdf: "/pdfs/english/7th english  unit -1 LEARNING TOGETHER.pdf", about: "Understand the basics of nouns, pronouns, and their usage in sentences." },
//       2: { title: "Wit And Humour", file: "/videos/english/7th english unit -1 LEARNING TOGETHER.mp4", pdf: "/pdfs/english/7th english unit -2 WIT AND HUMOUR.pdf", about: "Explore verbs, different tenses, and how they change meaning." },
//       3: { title: "Dreams And Discoveries", file: "/videos/english/english_3.mp4", pdf: "/pdfs/english/7th english unit -3 DREAMS & DISCOVERS.pdf", about: "Learn to identify and use adjectives and adverbs to describe words effectively." },
//       4: { title: "Travel And Adventure", file: "/videos/english/english_4.mp4", pdf: "/pdfs/english/7th english unit -4 TRAVEL & ADVENTURE.pdf", about: "Understand the role of prepositions in showing relationships and conjunctions in joining sentences." },
//       5: { title: "Brave Hearts", file: "/videos/english/english_5.mp4", pdf: "/pdfs/english/7th english unit -5 BRAVEHEARTS.pdf", about: "Master different sentence structures and the correct use of punctuation marks." },
//     },
//     Computer: {
//       1: { title: "Microsoft word", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/computer/computer-ch1.pdf", about: "Microsoft Word is a word-processing software used to create, edit, format, and share text documents." },
//       2: { title: "Text Editing", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/computer/computer-ch2.pdf", about: "Text editing is the process of creating, modifying, and formatting written content using a text editor or word processor." },
//       3: { title: "MS Word Pictures", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/computer/computer-ch3.pdf", about: "Microsoft Word, pictures can be inserted and formatted to enhance the appearance and meaning of a document." },
//       4: { title: "MS Word Smart Art", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/computer/computer-ch4.pdf", about: "SmartArt in Microsoft Word is a feature that lets you create diagrams and visuals to represent information effectively." },
//       5: { title: "Smart Art Editing", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/computer/computer-ch5.pdf", about: "SmartArt editing in Microsoft Word allows you to modify shapes, colors, layouts, and text within a diagram to better present information." },
//     }
    
  
//     },
//     '8': {
//       Maths: {
//         1: { title: "A SQUARE AND A CUBE", file: "/videos/class8/Maths/chapter-1.mp4", pdf: "/pdfs/class8/maths/chapter1.pdf", about: "Learn about rational numbers, their properties, and operations." },
//         2: { title: "POWER PLAY", file: "/videos/class8/Maths/chapter-2.mp4", pdf: "/pdfs/class8/maths/chapter2.pdf", about: "Understand linear equations and how to solve them." },
//         3: { title: "A STORY OF NUMBERS", file: "/videos/class8/Maths/chapter-3.mp4", pdf: "/pdfs/class8/maths/chapter3.pdf", about: "Explore different types of quadrilaterals and their properties." },
//         4: { title: "QUADRILATERALS", file: "/videos/class8/Maths/chapter-4.mp4", pdf: "/pdfs/class8/maths/chapter4.pdf", about: "Learn about data collection, organization, and representation." },
//         5: { title: "NUMBER PLAY", file: "/videos/class8/Maths/chapter-5.mp4", pdf: "/pdfs/class8/maths/chapter5.pdf", about: "Understand squares, square roots, and their applications." },
//       },
//       Science: {
//         1: { title: "particulate nature of matter", file: "/videos/class8/Science/chapter-1.mp4", pdf: "/pdfs/class8/science/chapter1.pdf", about: "Learn about agricultural practices and crop production methods." },
//         2: { title: "Beyond our naked eye", file: "/videos/class8/Science/chapter-2.mp4", pdf: "/pdfs/class8/science/chapter2.pdf", about: "Explore the world of microorganisms and their importance." },
//         3: { title: "The ultimate treasure", file: "/videos/class8/Science/chapter-3.mp4", pdf: "/pdfs/class8/science/chapter3.pdf", about: "Understand synthetic fibers, their properties, and uses." },
//         4: { title: "magnetic and heating effects", file: "/videos/class8/Science/chapter-4.mp4", pdf: "/pdfs/class8/science/chapter4.pdf", about: "Study the properties and uses of metals and non-metals." },
//         5: { title: "Exploring Forces", file: "/videos/class8/Science/chapter-5.mp4", pdf: "/pdfs/class8/science/chapter5.pdf", about: "Learn about fossil fuels like coal and petroleum." },
//       },
//          Social: {
//       1: { title: "Natural Resourses", file: "/videos/social/chapter1 (online-video-cutter.com).mp4", pdf: "/pdfs/class8/scoial/chapter1.pdf", about: "Explore historical changes and sources over a thousand years in India." },
//       2: { title: "Reshaping india's Political Map", file: "/videos/social/chpter2social.mp4", pdf: "/pdfs/class8/scoial/chapter2.pdf", about: "Learn about the rise of various kingdoms in medieval India." },
//       3: { title: "The Colonical Era in India", file: "/videos/social/social_ch3.mp4.mp4", pdf: "/pdfs/class8/scoial/chapter3.pdf", about: "Know about the Delhi Sultans, their administration, and monuments." },
//       4: { title: "The Parliamentary System:legislature and Executive", file: "/videos/social/social_ch4.mp4.mp4", pdf: "/pdfs/class8/scoial/chapter4.pdf", about: "A detailed look into the Mughal Empire, its rulers, and policies." },
//       5: { title: "Universal Franchise and India's Electoral System", file: "/videos/social/social_ch5.mp4.mp4", pdf: "/pdfs/class8/scoial/chapter5.pdf", about: "Study the architectural marvels and ruling strategies of various historical rulers." },
//     },
//     English: {
//       1: { title: "Wit And Wisdom", file: "/videos/english/7th english unit -1 LEARNING TOGETHER (2).mp4", pdf: "/pdfs/class8/english/chapter1.pdf", about: "Understand the basics of nouns, pronouns, and their usage in sentences." },
//       2: { title: "Values And Dispositions", file: "/videos/english/7th english unit -1 LEARNING TOGETHER.mp4", pdf: "/pdfs/class8/english/chapter2.pdf", about: "Explore verbs, different tenses, and how they change meaning." },
//       3: { title: "Mystery And Magic", file: "/videos/english/english_3.mp4", pdf: "/pdfs/class8/english/chapter3.pdf", about: "Learn to identify and use adjectives and adverbs to describe words effectively." },
//       4: { title: "Environment", file: "/videos/english/english_4.mp4", pdf: "/pdfs/class8/english/chapter4.pdf", about: "Understand the role of prepositions in showing relationships and conjunctions in joining sentences." },
//       5: { title: "Science And Curiosity", file: "/videos/english/english_5.mp4", pdf: "/pdfs/class8/english/chapter5.pdf", about: "Master different sentence structures and the correct use of punctuation marks." },
//     },
//     Computer: {
//       1: { title: "Exception handling in python", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class8/computer/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "File handling In python", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class8/computer/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "Stack", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class8/computer/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "Queue", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class8/computer/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "Sorting", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class8/computer/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },

//       // Add other subjects for Class 8
//     },
//     '9': {
//       // Add videos for Class 9 subjects
//         Maths: {
//       1: { title: "Number systems", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class9/maths/chapter1.pdf", about: "Microsoft Word is a word-processing software used to create, edit, format, and share text documents." },
//       2: { title: "Polynomials", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class9/maths/chapter2.pdf", about: "Text editing is the process of creating, modifying, and formatting written content using a text editor or word processor." },
//       3: { title: "COORDINATE GEOMETRY", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class9/maths/chapter3.pdf", about: "Microsoft Word, pictures can be inserted and formatted to enhance the appearance and meaning of a document." },
//       4: { title: "LINEAR EQUATIONS", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class9/maths/chapter4.pdf", about: "SmartArt in Microsoft Word is a feature that lets you create diagrams and visuals to represent information effectively." },
//       5: { title: "INTRODUCTION TO EUCLIDS GEOMETRY", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class9/maths/chapter5.pdf", about: "SmartArt editing in Microsoft Word allows you to modify shapes, colors, layouts, and text within a diagram to better present information." },
//     },
//      Science: {
//       1: { title: "MATTER IN OUR SURROUNDINGS", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class9/science/chapter1.pdf", about: "Matter is anything that has mass and occupies space. It exists in various states, including solid, liquid, and gas." },
//       2: { title: "Motion", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class9/science/chapter4.pdf", about: "Motion is the change in position of an object with respect to time. It can be described in terms of speed, velocity, and acceleration." },
//       3: { title: "Atoms and Molecules", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class9/science/chapter2.pdf", about: "Atoms and molecules are the building blocks of matter, with atoms being the smallest units of elements and molecules being combinations of atoms." },
//       4: { title: "Gravitation", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class9/science/chapter5.pdf", about: "Gravitation is a natural phenomenon by which all things with mass are brought toward one another, including planets, stars, galaxies, and even light." },
//       5: { title: "The fundamentals of Life", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class9/science/chapter3.pdf", about: "The fundamentals of life include the basic characteristics and processes that define living organisms, such as growth, reproduction, and response to stimuli." },
//     },
//      English: {
//       1: { title: "NOTES FOR THE TEACHER", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class9/english/lesson-1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "THE SOUND OF THE MUSIC", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class9/english/lesson-2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "LITTLE GIRL", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class9/english/lesson-3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "A TRULY BEAUTIFUL MIND", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class9/english/lesson-4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "THE SNAKE AND THE MIRROR", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class9/english/lesson-5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//      Social: {
//       1: { title: "Democracy Rights ch1", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class9/social/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "Constitutional Rights", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class9/social/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "Electoral Politics", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class9/social/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "Electorial Politics and Institutions", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class9/social/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "Democracy Rights ch2", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class9/social/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//      Computer: {
//       1: { title: "INTODUCTION TO ICT", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class9/computer/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "CREATING TEXTUAL COMMUNICATION", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class9/computer/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "CREATING VISUAL COMMUNICATION", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class9/computer/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "CREATING AUDIO VIDEO COMMUNICATION", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class9/computer/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "GETTING CONNECTED INTERNET", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class9/computer/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//     },
//     '10': {
//        Maths: {
//       1: { title: "Real Numbers", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class10/maths/chapter1.pdf", about: "Real numbers are all the numbers on the number line, including both rational and irrational numbers." },
//       2: { title: "polynomials", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class10/maths/chapter2.pdf", about: "Polynomials are algebraic expressions that consist of variables, coefficients, and exponents." },
//       3: { title: "Linear Equations", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class10/maths/chapter3.pdf", about: "A linear equation is an equation of the first degree, meaning it has no exponents greater than one." },
//       4: { title: "Quadratic Equations", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class10/maths/chapter4.pdf", about: "A quadratic equation is a second-degree polynomial equation in a single variable." },
//       5: { title: "Arithmetic Progressions", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class10/maths/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//      Science: {
//       1: { title: "CHEMICAL REACTIONS AND EQUATIONS", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class10/science/chapter1.pdf", about: "Chemical reactions involve the transformation of reactants into products, accompanied by energy changes." },
//       2: { title: "ACIDS, BASES AND SALTS", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class10/science/chapter2.pdf", about: "Acids, bases, and salts are three important classes of compounds in chemistry." },
//       3: { title: "METALS AND NON-METALS", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class10/science/chapter3.pdf", about: "Metals and non-metals are two distinct categories of elements with different properties." },
//       4: { title:"CARBON AND ITS COMPOUNDS", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class10/science/chapter4.pdf", about: "Carbon and its compounds form the basis of organic chemistry." },
//       5: { title: "PERIODIC CLASSIFICATION OF ELEMENTS", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class10/science/chapter5.pdf", about: "The periodic table organizes elements based on their atomic number and properties." },
//     },
//      English: {
//       1: { title: "Exploring the investigative world of science", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class10/english/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "Beyond our naked eye", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class10/english/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "The ultimate Treasure", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class10/english/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "magnetic and heating effects", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class10/english/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "Exploring Forces", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class10/english/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//      Social: {
//       1: { title: "Resourses GNP PTVTLOFMTNT", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class10/social/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "Forest and wildlife resourses", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class10/social/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "Lifelines of national economy", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class10/social/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "Agriculture", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class10/social/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "Manufacturing Industries", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class10/social/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },
//      Computer: {
//       1: { title: "Introduction To ICT", file: "/videos/Computer/chapter-1.mp4", pdf: "/pdfs/class10/computer/chapter1.pdf", about: "Exception handling in Python is a mechanism to handle runtime errors, allowing the program to continue execution." },
//       2: { title: "Creating Textual Communication", file: "/videos/Computer/chapter-2.mp4", pdf: "/pdfs/class10/computer/chapter2.pdf", about: "File handling in Python allows you to read from and write to files, enabling data persistence." },
//       3: { title: "Creating Visual Communication", file: "/videos/Computer/chapter-3.mp4", pdf: "/pdfs/class10/computer/chapter3.pdf", about: "A stack is a linear data structure that follows the Last In First Out (LIFO) principle." },
//       4: { title: "Creating Audio Video Communication", file: "/videos/Computer/chapter-4.mp4", pdf: "/pdfs/class10/computer/chapter4.pdf", about: "A queue is a linear data structure that follows the First In First Out (FIFO) principle." },
//       5: { title: "Getting Connected Internet", file: "/videos/Computer/chapter-5.mp4", pdf: "/pdfs/class10/computer/chapter5.pdf", about: "Sorting is the process of arranging data in a specific order, typically in ascending or descending order." },
//     },// Add videos for Class 10 subjects
//     }
//   };

//   const currentLesson = videos[classNumber]?.[subject]?.[chapterNumber] || {
//     title: "Lesson Not Found",
//     file: "",
//     about: ""
//   };

//   const questions = quizQuestions[classNumber]?.[subject]?.[chapterNumber] || [];

//   const lessons = Object.keys(videos[classNumber]?.[subject] || {}).map((id) => ({
//     id,
//     title: videos[classNumber][subject][id].title,
//     status: parseInt(id) < parseInt(chapterNumber) ? "completed" 
//            : parseInt(id) === parseInt(chapterNumber) ? "current" : "next"
//   }));

//   const checklistItems = [
//     { id: 1, task: `Watch full video of ${currentLesson.title}`, status: checklistStatus.videoWatched ? "completed" : "in-progress" },
//     { id: 2, task: "Attempt practice quiz", status: checklistStatus.practiceAttempted ? "completed" : "pending" },
//   ];

//   const practiceQuestions = [
//     { id: 1, question: `Practice questions for ${currentLesson.title}` },
//   ];

//   const handleSeek = (time) => {
//     if (videoRef.current) {
//       videoRef.current.currentTime = time;
//       videoRef.current.play();
//     }
//   };

//   const handleGoBack = () => {
//     navigate(`/learn/class${classNumber}`);
//   };

//   const handleChapterClick = (chapterId) => {
//     navigate(`/lesson/${classNumber}/${subject}/${chapterId}`);
//   };

//   const handleVideoEnd = () => {
//     setIsVideoCompleted(true);
//   };

//   const handleStartQuiz = () => {
//     if (remainingChances > 0) {
//       setShowQuiz(true);
//       setCurrentQuestionIndex(0);
//       setSelectedAnswer(null);
//       setQuizScore(0);
//       setQuizCompleted(false);
//     }
//   };

//   const handleAnswerSelect = (index) => {
//     setSelectedAnswer(index);
//   };

//   const handleNextQuestion = () => {
//     if (selectedAnswer === questions[currentQuestionIndex].correctAnswer) {
//       setQuizScore(prevScore => prevScore + 1);
//     }
//     if (currentQuestionIndex < questions.length - 1) {
//       setCurrentQuestionIndex(currentQuestionIndex + 1);
//       setSelectedAnswer(null);
//     } else {
//       setQuizCompleted(true);
//       const newChances = remainingChances - 1;
//       setRemainingChances(newChances);
      
//       // Update localStorage with chapter-specific key
//       const chapterKey = getChapterKey();
//       localStorage.setItem(chapterKey, newChances.toString());
      
//       const finalScore = quizScore + (selectedAnswer === questions[currentQuestionIndex].correctAnswer ? 1 : 0);
//       const isPassed = finalScore >= Math.ceil(questions.length * 0.8);
//       setChecklistStatus(prev => ({
//         ...prev,
//         practiceAttempted: true,
//         quizPassed: isPassed
//       }));
//     }
//   };

//   const handleCloseQuiz = () => {
//     setShowQuiz(false);
//   };

//   const handleRetryQuiz = () => {
//     if (remainingChances > 0) {
//       setCurrentQuestionIndex(0);
//       setSelectedAnswer(null);
//       setQuizScore(0);
//       setQuizCompleted(false);
//     }
//   }
// return (
//     <>
//       {/* Responsive styles */}
//       <style>
//       {`
//         .lesson-content {
//           display: flex;
//           gap: 24px;
//           padding: 24px;
//         }
//         .lesson-left {
//           flex: 2;
//           min-width: 0;
//         }
//         .lesson-right {
//           width: 320px;
//           min-width: 320px;
//         }
//         @media (max-width: 768px) {
//           .lesson-content {
//             flex-direction: column;
//             gap: 0;
//             padding: 12px;
//           }
//           .lesson-left,
//           .lesson-right {
//             width: 100%;
//             min-width: 0;
//           }
//           .lesson-right {
//             display: flex;
//             flex-direction: column;
//             gap: 16px;
//             width: 100%;
//             min-width: 0;
//             margin-top: 20px;
//           }
//           .lesson-right > div {
//             width: 100%;
//           }
//         }
//         /* Hide download button from video controls */
//         video::-webkit-media-controls-download-button {
//           display: none;
//         }
//         video::-webkit-media-controls-enclosure {
//           overflow: hidden;
//         }
//         video::-moz-media-controls-panel {
//           display: flex;
//         }
//         video::-moz-media-controls-download-button {
//           display: none;
//         }
//         /* Additional CSS to ensure download option is hidden */
//         video {
//           controlsList: "nodownload";
//         }
//       `}
//       </style>
//       <div style={{ fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
//         {/* Header */}
//         <div style={{ backgroundColor: 'white', padding: '100px 32px', borderBottom: '1px solid #e5e7eb',
//                       display: 'flex', alignItems: 'center', gap: '16px' }}>
//           <ArrowLeft size={20} style={{ cursor: 'pointer', color: '#6b7280', }} onClick={handleGoBack} />
//           <h1 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>
//             {subject} • {currentLesson.title}
//           </h1>
//         </div>
//         <div className="lesson-content">
//           {/* Left section: video, about, PDF, checklist, practice */}
//           <div className="lesson-left">
//             <div style={{ marginBottom: '24px' }}>
//               <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
//                 Video: {currentLesson.title}
//               </h2>
//               <video
//                 ref={videoRef}
//                 src={currentLesson.file}
//                 controls
//                 controlsList="nodownload"
//                 width="100%"
//                 style={{ borderRadius: "8px", backgroundColor: "#000", marginTop: "12px" }}
//                 onTimeUpdate={(e) => setCurrentTime(e.target.currentTime)}
//                 onEnded={handleVideoEnd}
//               />
//             </div>
//             <div style={{ backgroundColor: "white", padding: "16px", borderRadius: "8px", marginBottom: "20px", border: "1px solid #e5e7eb" }}>
//               <h3 style={{ fontSize: "18px", fontWeight: "600", marginBottom: "10px", color: "#1f2937" }}>📘 About</h3>
//               <p style={{ fontSize: "14px", color: "#4b5563", lineHeight: "1.6" }}>
//                 {currentLesson.about || "No description available."}
//               </p>
//             </div>
//             {currentLesson.pdf && (
//               <div style={{ marginTop: "20px" }}>
//                 {!showPdf && (
//                   <button
//                     onClick={() => setShowPdf(true)}
//                     style={{
//                       backgroundColor: "#0f766e",
//                       color: "white",
//                       padding: "10px 16px",
//                       border: "none",
//                       borderRadius: "6px",
//                       cursor: "pointer",
//                       fontSize: "14px",
//                     }}
//                   >
//                     📖 View Lesson PDF
//                   </button>
//                 )}
//                 {showPdf && (
//                   <div>
//                     <iframe
//                       id="lessonPdfFrame"
//                       src={`${currentLesson.pdf}#view=FitH&scrollbar=1&toolbar=0`}
//                       title="Lesson PDF"
//                       style={{
//                         width: "100%",
//                         height: "500px",
//                         border: "1px solid #e5e7eb",
//                         borderRadius: "8px",
//                         overflow: "auto",
//                       }}
//                     />
//                     <div style={{ marginTop: "12px", display: "flex", gap: "10px" }}>
//                       <a
//                         href={currentLesson.pdf}
//                         download
//                         style={{
//                           backgroundColor: "#0f766e",
//                           color: "white",
//                           textDecoration: "none",
//                           padding: "10px 16px",
//                           borderRadius: "6px",
//                           fontSize: "14px",
//                           cursor: "pointer",
//                         }}
//                       >
//                         📥 Download Lesson PDF
//                       </a>
//                       <button
//                         onClick={() => setShowPdf(false)}
//                         style={{
//                           backgroundColor: "#dc2626",
//                           color: "white",
//                           padding: "10px 16px",
//                           border: "none",
//                           borderRadius: "6px",
//                           cursor: "pointer",
//                           fontSize: "14px",
//                         }}
//                       >
//                         ❌ Close PDF
//                       </button>
//                     </div>
//                   </div>
//                 )}
//               </div>
//             )}
//             <div style={{ display: 'flex', gap: '24px', marginTop: "24px", flexWrap: 'wrap' }}>
//               <div style={{
//                 flex: 1,
//                 backgroundColor: 'white',
//                 borderRadius: '12px',
//                 boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
//                 padding: '20px',
//                 border: '1px solid #e5e7eb',
//                 marginBottom: '20px'
//               }}>
//                 <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
//                   <FileText size={20}/> Lesson Checklist
//                 </h3>
//                 {checklistItems.map((item) => (
//                   <div key={item.id} style={{ padding: '12px 0', borderBottom: '1px solid #f3f4f6', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
//                     <span style={{ fontSize: '14px', color: '#4b5563' }}>{item.task}</span>
//                     <span style={{ 
//                       fontSize: '12px', 
//                       padding: '4px 8px', 
//                       borderRadius: '12px',
//                       background: item.status === "completed" ? "#10b981" : 
//                                  item.status === "in-progress" ? "#ec4899" : "#e5e7eb",
//                       color: item.status === "completed" || item.status === "in-progress" ? "white" : "#6b7280" 
//                     }}>
//                       {item.status}
//                     </span>
//                   </div>
//                 ))}
//               </div>
//               <div style={{
//                 flex: 1,
//                 backgroundColor: 'white',
//                 borderRadius: '12px',
//                 boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
//                 padding: '20px',
//                 border: '1px solid #e5e7eb',
//                 marginBottom: '20px'
//               }}>
//                 <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>
//                   Quick Practice
//                 </h3>
//                 <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
//                   <AlertCircle size={16} color="#f59e0b" />
//                   <span style={{ fontSize: '14px', color: '#f59e0b' }}>
//                     {remainingChances} {remainingChances === 1 ? 'chance' : 'chances'} remaining for this chapter
//                   </span>
//                 </div>
//                 {practiceQuestions.map((q) => (
//                   <div key={q.id} style={{ padding: '12px 0', borderBottom: '1px solid #f3f4f6', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
//                     <span style={{ fontSize: '14px', color: '#4b5563' }}>{q.question}</span>
//                     <button 
//                       onClick={handleStartQuiz}
//                       disabled={remainingChances <= 0}
//                       style={{ 
//                         backgroundColor: remainingChances > 0 ? "#0f766e" : "#9ca3af", 
//                         color: "white", 
//                         border: "none", 
//                         borderRadius: "4px", 
//                         padding: "6px 12px",
//                         cursor: remainingChances > 0 ? "pointer" : "not-allowed",
//                         display: "flex",
//                         alignItems: "center",
//                         gap: "4px"
//                       }}
//                     >
//                       <Play size={14} />
//                       {remainingChances > 0 ? "Start" : "No chances"}
//                     </button>
//                   </div>
//                 ))}
//               </div>
//             </div>
//           </div>
//           {/* Right section: lesson outline and AI assistant (now appears below video on mobile) */}
//           <div className="lesson-right">
//             <div style={{ 
//               backgroundColor: 'white',
//               borderRadius: '12px',
//               boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
//               padding: '20px',
//               marginBottom: '20px',
//               border: '1px solid #e5e7eb'
//             }}>
//               <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', margin: '0 0 16px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
//                 <FileText size={20} />
//                 Lesson Outline
//               </h3>
//               {lessons.map((lesson) => (
//                 <div 
//                   key={lesson.id} 
//                   onClick={() => handleChapterClick(lesson.id)}
//                   style={{
//                     display: 'flex',
//                     alignItems: 'center',
//                     padding: '12px 0',
//                     cursor: 'pointer',
//                     transition: 'background-color 0.2s',
//                     borderRadius: '6px',
//                     paddingLeft: '8px',
//                     margin: '0 -8px'
//                   }}
//                   onMouseEnter={(e) => {
//                     e.currentTarget.style.backgroundColor = '#f9fafb';
//                   }}
//                   onMouseLeave={(e) => {
//                     e.currentTarget.style.backgroundColor = 'transparent';
//                   }}
//                 >
//                   <div style={{ display: 'flex', alignItems: 'center', flex: 1, gap: '12px' }}>
//                     {lesson.status === 'completed' && <CheckCircle size={20} style={{ color: '#10b981' }} />}
//                     {lesson.status === 'current' && (
//                       <div style={{
//                         width: '20px',
//                         height: '20px',
//                         backgroundColor: '#ec4899',
//                         borderRadius: '50%',
//                         display: 'flex',
//                         alignItems: 'center',
//                         justifyContent: 'center'
//                       }}>
//                         <div style={{
//                           width: '6px',
//                           height: '6px',
//                           backgroundColor: 'white',
//                           borderRadius: '50%'
//                         }} />
//                       </div>
//                     )}
//                     {lesson.status === 'next' && <ChevronRight size={20} style={{ color: '#6b7280' }} />}
//                     {lesson.status === 'locked' && <Lock size={16} style={{ color: '#d1d5db' }} />}
//                     <div style={{ flex: 1 }}>
//                       <span style={{ color: '#6b7280', fontSize: '12px', marginRight: '8px' }}>{lesson.id}.</span>
//                       <span style={{ color: lesson.status === 'locked' ? '#d1d5db' : '#4b5563', fontSize: '14px', fontWeight: lesson.status === 'current' ? '600' : '400' }}>
//                         {lesson.title}
//                       </span>
//                     </div>
//                   </div>
//                   <span style={{
//                     backgroundColor: 
//                       lesson.status === 'completed' ? '#d1fae5' :
//                       lesson.status === 'current' ? '#fce7f3' : 
//                       lesson.status === 'next' ? '#e0f2fe' : '#f3f4f6',
//                     color: 
//                       lesson.status === 'completed' ? '#10b981' :
//                       lesson.status === 'current' ? '#ec4899' :
//                       lesson.status === 'next' ? '#0284c7' : '#9ca3af',
//                     padding: '4px 8px',
//                     borderRadius: '12px',
//                     fontSize: '10px',
//                     fontWeight: '500',
//                     textTransform: 'capitalize'
//                   }}>
//                     {lesson.status === 'completed' ? 'Completed' :
//                      lesson.status === 'current' ? 'Current' :
//                      lesson.status === 'next' ? 'Next' : 'Locked'}
//                   </span>
//                 </div>
//               ))}
//             </div>
//             <div style={{
//               backgroundColor: 'white',
//               borderRadius: '12px',
//               boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
//               padding: '20px',
//               border: '1px solid #e5e7eb'
//             }}>
//               <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
//                 <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#1f2937', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
//                   <MessageCircle size={18} style={{ color: '#ec4899' }} />
//                   AI Learning Assistant
//                 </h3>
//                 <button style={{ backgroundColor: '#f3f4f6', color: '#6b7280', border: 'none', padding: '6px 12px', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>
//                   Ask
//                 </button>
//               </div>
//               <p style={{ color: '#6b7280', fontSize: '14px', margin: '0 0 12px 0' }}>
//                 Need help? Ask about any step you're stuck on.
//               </p>
//               <div style={{ backgroundColor: '#fef3c7', border: '1px solid #f59e0b', borderRadius: '6px', padding: '12px', marginBottom: '12px' }}>
//                 <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
//                   <span style={{ fontSize: '16px' }}>💡</span>
//                   <span style={{ fontSize: '12px', fontWeight: '600', color: '#92400e' }}>Tip</span>
//                 </div>
//                 <p style={{ fontSize: '12px', color: '#92400e', margin: 0 }}>
//                   Try a practice question on factoring after the video.
//                 </p>
//               </div>
//               <textarea
//                 placeholder="Type your question..."
//                 style={{ width: '100%', height: '60px', border: '1px solid #d1d5db', borderRadius: '6px', padding: '8px', fontSize: '14px', resize: 'none', marginBottom: '12px' }}
//               />
//               <button style={{ width: '100%', backgroundColor: '#0f766e', color: 'white', border: 'none', padding: '10px', borderRadius: '6px', fontSize: '14px', fontWeight: '600', cursor: 'pointer' }}>
//                 Send
//               </button>
//             </div>
//           </div>
//         </div>
//         {/* Quiz Modal */}
//         {showQuiz && (
//           <div style={{
//             position: 'fixed',
//             top: 0,
//             left: 0,
//             right: 0,
//             bottom: 0,
//             backgroundColor: 'rgba(0, 0, 0, 0.5)',
//             display: 'flex',
//             alignItems: 'center',
//             justifyContent: 'center',
//             zIndex: 1000
//           }}>
//             <div style={{
//               backgroundColor: 'white',
//               borderRadius: '8px',
//               padding: '24px',
//               width: '90%',
//               maxWidth: '600px',
//               maxHeight: '90vh',
//               overflow: 'auto',
//               position: 'relative'
//             }}>
//               <button 
//                 onClick={handleCloseQuiz}
//                 style={{
//                   position: 'absolute',
//                   top: '16px',
//                   right: '16px',
//                   background: 'none',
//                   border: 'none',
//                   cursor: 'pointer'
//                 }}
//               >
//                 <X size={20} color="#6b7280" />
//               </button>
//               {!quizCompleted ? (
//                 <>
//                   <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
//                     Question {currentQuestionIndex + 1} of {questions.length}
//                   </h2>
//                   <p style={{ fontSize: '18px', marginBottom: '24px', fontWeight: '500' }}>
//                     {questions[currentQuestionIndex]?.question}
//                   </p>
//                   <div style={{ marginBottom: '24px' }}>
//                     {questions[currentQuestionIndex]?.options.map((option, index) => (
//                       <div 
//                         key={index}
//                         onClick={() => handleAnswerSelect(index)}
//                         style={{
//                           padding: '12px 16px',
//                           border: `2px solid ${selectedAnswer === index ? '#0f766e' : '#e5e7eb'}`,
//                           borderRadius: '8px',
//                           marginBottom: '12px',
//                           cursor: 'pointer',
//                           backgroundColor: selectedAnswer === index ? '#f0fdfa' : 'white',
//                           transition: 'all 0.2s'
//                         }}
//                       >
//                         {option}
//                       </div>
//                     ))}
//                   </div>
//                   <button 
//                     onClick={handleNextQuestion}
//                     disabled={selectedAnswer === null}
//                     style={{
//                       width: '100%',
//                       padding: '12px',
//                       backgroundColor: selectedAnswer !== null ? '#0f766e' : '#9ca3af',
//                       color: 'white',
//                       border: 'none',
//                       borderRadius: '6px',
//                       fontSize: '16px',
//                       fontWeight: '600',
//                       cursor: selectedAnswer !== null ? 'pointer' : 'not-allowed'
//                     }}
//                   >
//                     {currentQuestionIndex === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
//                   </button>
//                 </>
//               ) : (
//                 <>
//                   <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
//                     Quiz Completed!
//                   </h2>
//                   <div style={{ 
//                     textAlign: 'center', 
//                     padding: '24px', 
//                     backgroundColor: '#f0fdfa', 
//                     borderRadius: '8px',
//                     marginBottom: '24px'
//                   }}>
//                     <p style={{ fontSize: '18px', marginBottom: '8px' }}>
//                       Your score: {quizScore} out of {questions.length}
//                     </p>
//                     <p style={{ fontSize: '16px', color: '#4b5563' }}>
//                       {quizScore >= Math.ceil(questions.length * 0.8) 
//                         ? 'Congratulations! You passed the quiz.' 
//                         : 'Keep studying and try again.'}
//                     </p>
//                   </div>
//                   <div style={{ display: 'flex', gap: '12px' }}>
//                     <button 
//                       onClick={handleCloseQuiz}
//                       style={{
//                         flex: 1,
//                         padding: '12px',
//                         backgroundColor: '#e5e7eb',
//                         color: '#4b5563',
//                         border: 'none',
//                         borderRadius: '6px',
//                         fontSize: '16px',
//                         fontWeight: '600',
//                         cursor: 'pointer'
//                       }}
//                     >
//                       Close
//                     </button>
//                     {remainingChances > 0 && quizScore < Math.ceil(questions.length * 0.8) && (
//                       <button 
//                         onClick={handleRetryQuiz}
//                         style={{
//                           flex: 1,
//                           padding: '12px',
//                           backgroundColor: '#0f766e',
//                           color: 'white',
//                           border: 'none',
//                           borderRadius: '6px',
//                           fontSize: '16px',
//                           fontWeight: '600',
//                           cursor: 'pointer'
//                         }}
//                       >
//                         Try Again ({remainingChances} left)
//                       </button>
//                     )}
//                   </div>
//                 </>
//               )}
//             </div>
//           </div>
//         )}
//       </div>
//       <style>
//       {`
//         .lesson-pdf-frame {
//           width: 100% !important;
//           min-height: 400px !important;
//           max-height: 75vh !important;
//           border: 1px solid #e5e7eb !important;
//           border-radius: 8px !important;
//           background: white !important;
//         }
//         @media (max-width: 768px) {
//           .lesson-pdf-frame {
//             height: 60vh !important;
//             min-height: 250px !important;
//             max-height: 75vh !important;
//           }
//         }
//       `}
//       </style>
//     </>
//   );
// };

// export default LessonPage;





import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { 
  ArrowLeft, 
  CheckCircle, 
  FileText, 
  MessageCircle, 
  Lock, 
  ChevronRight,
  X,
  AlertCircle,
  Play,
  Send,
  Bot,
  User,
  Calendar,
  Lightbulb,
  BookOpen
} from 'lucide-react';

const LessonPage = () => {
  const { class: classNumber, subject, chapterNumber } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const videoRef = useRef(null);
  const chatContainerRef = useRef(null);
  const [isVideoCompleted, setIsVideoCompleted] = useState(false);
  const [showPdf, setShowPdf] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [quizScore, setQuizScore] = useState(0);
  const [quizCompleted, setQuizCompleted] = useState(false);
  const [remainingChances, setRemainingChances] = useState(3);
  
  // AI Assistant States
  const [chatMessages, setChatMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showQuickActions, setShowQuickActions] = useState(true);

  // Centralized state for the checklist
  const [checklistStatus, setChecklistStatus] = useState({
    videoWatched: false,
    practiceAttempted: false,
    quizPassed: false
  });

  // Get chapter title and subtopic from URL parameters
  const queryParams = new URLSearchParams(location.search);
  const chapterTitle = queryParams.get('chapterTitle') || `Chapter ${chapterNumber}`;
  const subtopicName = queryParams.get('subtopic');

  // Generate unique key for each chapter's quiz chances
  const getChapterKey = () => `quiz_chances_${classNumber}_${subject}_${chapterNumber}`;
  const getChapterDateKey = () => `quiz_date_${classNumber}_${subject}_${chapterNumber}`;

  useEffect(() => {
    const today = new Date().toDateString();
    const chapterKey = getChapterKey();
    const chapterDateKey = getChapterDateKey();
    
    const storedDate = localStorage.getItem(chapterDateKey);
    const storedChances = localStorage.getItem(chapterKey);
    
    if (storedDate === today) {
      setRemainingChances(parseInt(storedChances) || 3);
    } else {
      setRemainingChances(3);
      localStorage.setItem(chapterKey, '3');
      localStorage.setItem(chapterDateKey, today);
    }
  }, [classNumber, subject, chapterNumber]);

  // Update checklist when video is completed
  useEffect(() => {
    if (isVideoCompleted) {
      setChecklistStatus(prev => ({
        ...prev,
        videoWatched: true
      }));
    }
  }, [isVideoCompleted]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatMessages, isLoading]);

  // Current lesson data
  const currentLesson = {
    title: chapterTitle,
    subtopic: subtopicName,
    file: `/videos/${subject}/chapter-${chapterNumber}.mp4`,
    pdf: `/pdfs/${subject}/chapter-${chapterNumber}.pdf`,
    about: `Learn about ${subject} concepts in ${chapterTitle}${subtopicName ? ` - ${subtopicName}` : ''}. This ${subtopicName ? 'subtopic' : 'chapter'} covers important topics that will help you build a strong foundation.`
  };

  // Sample lessons for outline
  const lessons = [
    { id: '1', title: 'Introduction to Concepts', status: 'completed' },
    { id: '2', title: 'Core Principles', status: 'completed' },
    { id: '3', title: 'Advanced Applications', status: 'current' },
    { id: '4', title: 'Practice Exercises', status: 'next' },
    { id: '5', title: 'Chapter Review', status: 'next' }
  ];

  const checklistItems = [
    { id: 1, task: `Watch full video of ${currentLesson.title}`, status: checklistStatus.videoWatched ? "completed" : "in-progress" },
    { id: 2, task: "Attempt practice quiz", status: checklistStatus.practiceAttempted ? "completed" : "pending" },
  ];

  const practiceQuestions = [
    { id: 1, question: `Practice questions for ${currentLesson.title}` },
  ];

  const handleGoBack = () => {
    navigate(`/learn/class${classNumber}`);
  };

  const handleChapterClick = (chapterId) => {
    navigate(`/lesson/${classNumber}/${subject}/${chapterId}`);
  };

  const handleVideoEnd = () => {
    setIsVideoCompleted(true);
  };

  const handleStartQuiz = () => {
    if (remainingChances > 0) {
      setShowQuiz(true);
      setCurrentQuestionIndex(0);
      setSelectedAnswer(null);
      setQuizScore(0);
      setQuizCompleted(false);
    }
  };

  const handleAnswerSelect = (index) => {
    setSelectedAnswer(index);
  };

  const handleNextQuestion = () => {
    // Simulate quiz logic
    if (selectedAnswer === 0) { // Assume first answer is always correct for demo
      setQuizScore(prevScore => prevScore + 1);
    }
    if (currentQuestionIndex < 2) { // 3 questions for demo
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
    } else {
      setQuizCompleted(true);
      const newChances = remainingChances - 1;
      setRemainingChances(newChances);
      
      const chapterKey = getChapterKey();
      localStorage.setItem(chapterKey, newChances.toString());
      
      const isPassed = quizScore >= 2; // 2 out of 3 to pass
      setChecklistStatus(prev => ({
        ...prev,
        practiceAttempted: true,
        quizPassed: isPassed
      }));
    }
  };

  const handleCloseQuiz = () => {
    setShowQuiz(false);
  };

  const handleRetryQuiz = () => {
    if (remainingChances > 0) {
      setCurrentQuestionIndex(0);
      setSelectedAnswer(null);
      setQuizScore(0);
      setQuizCompleted(false);
    }
  };

  // AI Assistant Functions
  const sendMessage = async () => {
    if (!userInput.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: userInput.trim(),
      timestamp: new Date().toLocaleTimeString()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setUserInput('');
    setIsLoading(true);
    setShowQuickActions(false);

    try {
      const response = await fetch('http://localhost:8000/ai-assistant/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          class_level: `Class ${classNumber}`,
          subject: subject,
          chapter: currentLesson.title,
          student_question: userInput,
          chat_history: chatMessages
        }),
      });

      const data = await response.json();

      if (data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          type: 'assistant',
          content: data.response,
          messageType: data.type,
          timestamp: new Date().toLocaleTimeString()
        };
        setChatMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: "I'm sorry, I'm having trouble responding right now. Please try again later.",
        messageType: 'error',
        timestamp: new Date().toLocaleTimeString()
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = async (actionType) => {
    const messages = {
      study_plan: `Can you create a study plan for ${currentLesson.title} in ${subject}?`,
      notes: `Please provide comprehensive notes on ${currentLesson.title} in ${subject}`,
      explanation: `Can you explain the key concepts of ${currentLesson.title} in ${subject} in simple terms?`,
      practice: `Generate some practice questions for ${currentLesson.title} in ${subject}`
    };

    const message = messages[actionType];
    setUserInput(message);
    setTimeout(() => {
      sendMessage();
    }, 100);
  };

  const clearChat = () => {
    setChatMessages([]);
    setShowQuickActions(true);
  };

  // Format AI response with better styling
  const formatResponse = (content) => {
    return content.split('\n').map((line, index) => {
      if (line.startsWith('# ')) {
        return <h4 key={index} className="ai-response-heading">{line.replace('# ', '')}</h4>;
      } else if (line.startsWith('## ')) {
        return <h5 key={index} className="ai-response-subheading">{line.replace('## ', '')}</h5>;
      } else if (line.startsWith('- ') || line.startsWith('• ')) {
        return <div key={index} className="ai-response-list-item">• {line.replace(/^[-•]\s*/, '')}</div>;
      } else if (line.trim() === '') {
        return <br key={index} />;
      } else {
        return <div key={index} className="ai-response-text">{line}</div>;
      }
    });
  };

  // Demo quiz questions
  const demoQuestions = [
    {
      question: `What is the main topic covered in ${currentLesson.title}?`,
      options: ["Basic Concepts", "Advanced Applications", "Historical Context", "All of the above"],
      correctAnswer: 3
    },
    {
      question: "Which of the following best describes the learning objectives?",
      options: ["Memorization", "Conceptual Understanding", "Practical Application", "Both B and C"],
      correctAnswer: 3
    },
    {
      question: "What should you focus on while studying this chapter?",
      options: ["Key Definitions", "Problem Solving", "Real-world Applications", "All of the above"],
      correctAnswer: 3
    }
  ];

  return (
    <>
      <style>
        {`
          .lesson-content {
            display: flex;
            gap: 24px;
            padding: 24px;
          }
          .lesson-left {
            flex: 2;
            min-width: 0;
          }
          .lesson-right {
            width: 400px;
            min-width: 400px;
          }
          @media (max-width: 1024px) {
            .lesson-content {
              flex-direction: column;
              gap: 0;
              padding: 12px;
            }
            .lesson-left,
            .lesson-right {
              width: 100%;
              min-width: 0;
            }
            .lesson-right {
              display: flex;
              flex-direction: column;
              gap: 16px;
              width: 100%;
              min-width: 0;
              margin-top: 20px;
            }
            .lesson-right > div {
              width: 100%;
            }
          }
          video::-webkit-media-controls-download-button {
            display: none;
          }
          video::-webkit-media-controls-enclosure {
            overflow: hidden;
          }
          video {
            controlsList: "nodownload";
          }
          @keyframes bounce {
            0%, 80%, 100% {
              transform: scale(0);
            }
            40% {
              transform: scale(1);
            }
          }
          .lesson-pdf-frame {
            width: 100% !important;
            min-height: 400px !important;
            max-height: 75vh !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            background: white !important;
          }
          @media (max-width: 768px) {
            .lesson-pdf-frame {
              height: 60vh !important;
              min-height: 250px !important;
              max-height: 75vh !important;
            }
          }

          /* Header Styles */
          .lesson-header-subtitle {
            font-size: 14px;
            color: #6b7280;
            margin-top: 4px;
            font-weight: 500;
          }
          .lesson-header-title {
            display: flex;
            flex-direction: column;
            gap: 2px;
          }

          /* AI Assistant Styles */
          .ai-assistant-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
            height: 600px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
          }

          .ai-assistant-header {
            padding: 16px 20px;
            border-bottom: 1px solid #f1f5f9;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
          }

          .ai-assistant-title {
            font-size: 18px;
            font-weight: 600;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0;
          }

          .ai-chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #fafbfc;
            display: flex;
            flex-direction: column;
            gap: 16px;
          }

          .ai-chat-welcome {
            text-align: center;
            padding: 30px 20px;
            color: #64748b;
          }

          .ai-chat-welcome-icon {
            margin-bottom: 12px;
            opacity: 0.7;
          }

          .ai-chat-message {
            display: flex;
            gap: 12px;
            max-width: 100%;
          }

          .ai-chat-message.user {
            flex-direction: row-reverse;
          }

          .ai-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify: center;
            flex-shrink: 0;
            font-size: 14px;
          }

          .ai-avatar.user {
            background: #0f766e;
          }

          .ai-avatar.assistant {
            background: #ec4899;
          }

          .ai-message-bubble {
            max-width: 85%;
            padding: 14px 18px;
            border-radius: 18px;
            line-height: 1.5;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }

          .ai-message-bubble.user {
            background: #0f766e;
            color: white;
            border-bottom-right-radius: 6px;
          }

          .ai-message-bubble.assistant {
            background: white;
            color: #1e293b;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 6px;
          }

          .ai-message-timestamp {
            font-size: 11px;
            margin-top: 6px;
            opacity: 0.7;
          }

          .ai-message-bubble.user .ai-message-timestamp {
            text-align: right;
          }

          .ai-quick-actions {
            padding: 16px 20px;
            border-top: 1px solid #f1f5f9;
            background: white;
          }

          .ai-quick-actions-title {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 12px;
            font-weight: 500;
          }

          .ai-quick-actions-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
          }

          .ai-quick-action-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 10px 12px;
            background: #f8fafc;
            color: #0f766e;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
          }

          .ai-quick-action-btn:hover {
            background: #f0fdfa;
            border-color: #0f766e;
            transform: translateY(-1px);
          }

          .ai-input-container {
            padding: 16px 20px;
            border-top: 1px solid #f1f5f9;
            background: white;
          }

          .ai-input-wrapper {
            display: flex;
            gap: 12px;
            align-items: flex-end;
          }

          .ai-textarea {
            flex: 1;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 14px;
            resize: none;
            font-family: inherit;
            line-height: 1.5;
            background: #fafafa;
            transition: all 0.2s;
            min-height: 44px;
            max-height: 120px;
          }

          .ai-textarea:focus {
            outline: none;
            border-color: #0f766e;
            background: white;
            box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.1);
          }

          .ai-send-btn {
            background: #0f766e;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            min-height: 44px;
          }

          .ai-send-btn:hover:not(:disabled) {
            background: #0d645e;
            transform: translateY(-1px);
          }

          .ai-send-btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
            transform: none;
          }

          .ai-response-heading {
            color: #0f766e;
            margin: 8px 0;
            font-size: 15px;
            font-weight: 600;
          }

          .ai-response-subheading {
            color: #0f766e;
            margin: 6px 0;
            font-size: 14px;
            font-weight: 600;
          }

          .ai-response-list-item {
            margin: 4px 0;
            padding-left: 16px;
          }

          .ai-response-text {
            margin: 4px 0;
            line-height: 1.5;
          }

          .ai-typing-indicator {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .ai-typing-dots {
            display: flex;
            gap: 4px;
          }

          .ai-typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #9ca3af;
            animation: bounce 1.4s infinite ease-in-out;
          }

          .ai-typing-dot:nth-child(1) { animation-delay: -0.32s; }
          .ai-typing-dot:nth-child(2) { animation-delay: -0.16s; }
        `}
      </style>
      
      <div style={{ fontFamily: 'Arial, sans-serif', backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        {/* Header */}
        <div style={{ 
          backgroundColor: 'white', 
          padding: '100px 32px', 
          borderBottom: '1px solid #e5e7eb',
          display: 'flex', 
          alignItems: 'center', 
          gap: '16px' 
        }}>
          <ArrowLeft 
            size={20} 
            style={{ cursor: 'pointer', color: '#6b7280' }} 
            onClick={handleGoBack} 
          />
          <div className="lesson-header-title">
            <h1 style={{ fontSize: '20px', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>
              {subject} • {currentLesson.title}
            </h1>
            {currentLesson.subtopic && (
              <div className="lesson-header-subtitle">
                Topic: {currentLesson.subtopic}
              </div>
            )}
          </div>
        </div>

        <div className="lesson-content">
          {/* Left section: video, about, PDF, checklist, practice */}
          <div className="lesson-left">
            <div style={{ marginBottom: '24px' }}>
              <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937' }}>
                {currentLesson.subtopic ? `Video: ${currentLesson.subtopic}` : `Video: ${currentLesson.title}`}
              </h2>
              <video
                ref={videoRef}
                src={currentLesson.file}
                controls
                controlsList="nodownload"
                width="100%"
                style={{ borderRadius: "8px", backgroundColor: "#000", marginTop: "12px" }}
                onEnded={handleVideoEnd}
              />
            </div>

            <div style={{ 
              backgroundColor: "white", 
              padding: "16px", 
              borderRadius: "8px", 
              marginBottom: "20px", 
              border: "1px solid #e5e7eb" 
            }}>
              <h3 style={{ fontSize: "18px", fontWeight: "600", marginBottom: "10px", color: "#1f2937" }}>
                📘 About {currentLesson.subtopic ? 'this Topic' : 'this Chapter'}
              </h3>
              <p style={{ fontSize: "14px", color: "#4b5563", lineHeight: "1.6" }}>
                {currentLesson.about}
              </p>
            </div>

            {currentLesson.pdf && (
              <div style={{ marginTop: "20px" }}>
                {!showPdf && (
                  <button
                    onClick={() => setShowPdf(true)}
                    style={{
                      backgroundColor: "#0f766e",
                      color: "white",
                      padding: "10px 16px",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                      fontSize: "14px",
                    }}
                  >
                    📖 View Lesson PDF
                  </button>
                )}
                {showPdf && (
                  <div>
                    <iframe
                      src={`${currentLesson.pdf}#view=FitH&scrollbar=1&toolbar=0`}
                      title="Lesson PDF"
                      className="lesson-pdf-frame"
                    />
                    <div style={{ marginTop: "12px", display: "flex", gap: "10px" }}>
                      <a
                        href={currentLesson.pdf}
                        download
                        style={{
                          backgroundColor: "#0f766e",
                          color: "white",
                          textDecoration: "none",
                          padding: "10px 16px",
                          borderRadius: "6px",
                          fontSize: "14px",
                          cursor: "pointer",
                        }}
                      >
                        📥 Download Lesson PDF
                      </a>
                      <button
                        onClick={() => setShowPdf(false)}
                        style={{
                          backgroundColor: "#dc2626",
                          color: "white",
                          padding: "10px 16px",
                          border: "none",
                          borderRadius: "6px",
                          cursor: "pointer",
                          fontSize: "14px",
                        }}
                      >
                        ❌ Close PDF
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}

            <div style={{ display: 'flex', gap: '24px', marginTop: "24px", flexWrap: 'wrap' }}>
              {/* Checklist */}
              <div style={{
                flex: 1,
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
                padding: '20px',
                border: '1px solid #e5e7eb',
                marginBottom: '20px'
              }}>
                <h3 style={{ 
                  fontSize: '18px', 
                  fontWeight: '600', 
                  color: '#1f2937', 
                  marginBottom: '16px', 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '8px' 
                }}>
                  <FileText size={20}/> Lesson Checklist
                </h3>
                {checklistItems.map((item) => (
                  <div key={item.id} style={{ 
                    padding: '12px 0', 
                    borderBottom: '1px solid #f3f4f6', 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center' 
                  }}>
                    <span style={{ fontSize: '14px', color: '#4b5563' }}>{item.task}</span>
                    <span style={{ 
                      fontSize: '12px', 
                      padding: '4px 8px', 
                      borderRadius: '12px',
                      background: item.status === "completed" ? "#10b981" : 
                                 item.status === "in-progress" ? "#ec4899" : "#e5e7eb",
                      color: item.status === "completed" || item.status === "in-progress" ? "white" : "#6b7280" 
                    }}>
                      {item.status}
                    </span>
                  </div>
                ))}
              </div>

              {/* Quick Practice */}
              <div style={{
                flex: 1,
                backgroundColor: 'white',
                borderRadius: '12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
                padding: '20px',
                border: '1px solid #e5e7eb',
                marginBottom: '20px'
              }}>
                <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>
                  Quick Practice
                </h3>
                <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <AlertCircle size={16} color="#f59e0b" />
                  <span style={{ fontSize: '14px', color: '#f59e0b' }}>
                    {remainingChances} {remainingChances === 1 ? 'chance' : 'chances'} remaining for this chapter
                  </span>
                </div>
                {practiceQuestions.map((q) => (
                  <div key={q.id} style={{ 
                    padding: '12px 0', 
                    borderBottom: '1px solid #f3f4f6', 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center' 
                  }}>
                    <span style={{ fontSize: '14px', color: '#4b5563' }}>{q.question}</span>
                    <button 
                      onClick={handleStartQuiz}
                      disabled={remainingChances <= 0}
                      style={{ 
                        backgroundColor: remainingChances > 0 ? "#0f766e" : "#9ca3af", 
                        color: "white", 
                        border: "none", 
                        borderRadius: "4px", 
                        padding: "6px 12px",
                        cursor: remainingChances > 0 ? "pointer" : "not-allowed",
                        display: "flex",
                        alignItems: "center",
                        gap: "4px"
                      }}
                    >
                      <Play size={14} />
                      {remainingChances > 0 ? "Start" : "No chances"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right section: lesson outline and AI assistant */}
          <div className="lesson-right">
            {/* Lesson Outline */}
            <div style={{ 
              backgroundColor: 'white',
              borderRadius: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.03)',
              padding: '20px',
              marginBottom: '20px',
              border: '1px solid #e5e7eb'
            }}>
              <h3 style={{ 
                fontSize: '18px', 
                fontWeight: '600', 
                color: '#1f2937', 
                margin: '0 0 16px 0', 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px' 
              }}>
                <FileText size={20} />
                Lesson Outline
              </h3>
              {lessons.map((lesson) => (
                <div 
                  key={lesson.id} 
                  onClick={() => handleChapterClick(lesson.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    padding: '12px 0',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s',
                    borderRadius: '6px',
                    paddingLeft: '8px',
                    margin: '0 -8px'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#f9fafb';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', flex: 1, gap: '12px' }}>
                    {lesson.status === 'completed' && <CheckCircle size={20} style={{ color: '#10b981' }} />}
                    {lesson.status === 'current' && (
                      <div style={{
                        width: '20px',
                        height: '20px',
                        backgroundColor: '#ec4899',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <div style={{
                          width: '6px',
                          height: '6px',
                          backgroundColor: 'white',
                          borderRadius: '50%'
                        }} />
                      </div>
                    )}
                    {lesson.status === 'next' && <ChevronRight size={20} style={{ color: '#6b7280' }} />}
                    {lesson.status === 'locked' && <Lock size={16} style={{ color: '#d1d5db' }} />}
                    <div style={{ flex: 1 }}>
                      <span style={{ color: '#6b7280', fontSize: '12px', marginRight: '8px' }}>{lesson.id}.</span>
                      <span style={{ 
                        color: lesson.status === 'locked' ? '#d1d5db' : '#4b5563', 
                        fontSize: '14px', 
                        fontWeight: lesson.status === 'current' ? '600' : '400' 
                      }}>
                        {lesson.title}
                      </span>
                    </div>
                  </div>
                  <span style={{
                    backgroundColor: 
                      lesson.status === 'completed' ? '#d1fae5' :
                      lesson.status === 'current' ? '#fce7f3' : 
                      lesson.status === 'next' ? '#e0f2fe' : '#f3f4f6',
                    color: 
                      lesson.status === 'completed' ? '#10b981' :
                      lesson.status === 'current' ? '#ec4899' :
                      lesson.status === 'next' ? '#0284c7' : '#9ca3af',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '10px',
                    fontWeight: '500',
                    textTransform: 'capitalize'
                  }}>
                    {lesson.status === 'completed' ? 'Completed' :
                     lesson.status === 'current' ? 'Current' :
                     lesson.status === 'next' ? 'Next' : 'Locked'}
                  </span>
                </div>
              ))}
            </div>

            {/* AI Learning Assistant - Redesigned */}
            <div className="ai-assistant-container">
              {/* Header */}
              <div className="ai-assistant-header">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <h3 className="ai-assistant-title">
                    <MessageCircle size={20} style={{ color: '#ec4899' }} />
                    AI Learning Assistant
                  </h3>
                  {chatMessages.length > 0 && (
                    <button 
                      onClick={clearChat}
                      style={{ 
                        background: 'none', 
                        border: 'none', 
                        color: '#64748b', 
                        fontSize: '12px', 
                        cursor: 'pointer',
                        textDecoration: 'underline',
                        fontWeight: '500'
                      }}
                    >
                      Clear Chat
                    </button>
                  )}
                </div>
              </div>

              {/* Chat Messages */}
              <div 
                ref={chatContainerRef}
                className="ai-chat-container"
              >
                {chatMessages.length === 0 ? (
                  <div className="ai-chat-welcome">
                    <div className="ai-chat-welcome-icon">
                      <Bot size={40} />
                    </div>
                    <p style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: '500' }}>
                      Hello! I'm your AI Learning Assistant
                    </p>
                    <p style={{ margin: 0, fontSize: '14px', lineHeight: '1.4' }}>
                      Ask me anything about this lesson, request study plans and Notes.<br />
                    </p>
                  </div>
                ) : (
                  chatMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`ai-chat-message ${message.type}`}
                    >
                      <div className={`ai-avatar ${message.type}`}>
                        {message.type === 'user' ? <User size={18} /> : <Bot size={18} />}
                      </div>
                      <div className={`ai-message-bubble ${message.type}`}>
                        <div style={{ fontSize: '14px', lineHeight: '1.5' }}>
                          {message.type === 'assistant' ? formatResponse(message.content) : message.content}
                        </div>
                        <div className="ai-message-timestamp">
                          {message.timestamp}
                        </div>
                      </div>
                    </div>
                  ))
                )}
                
                {/* Typing Indicator */}
                {isLoading && (
                  <div className="ai-chat-message">
                    <div className="ai-avatar assistant">
                      <Bot size={18} />
                    </div>
                    <div className="ai-message-bubble assistant">
                      <div className="ai-typing-indicator">
                        <div className="ai-typing-dots">
                          <div className="ai-typing-dot"></div>
                          <div className="ai-typing-dot"></div>
                          <div className="ai-typing-dot"></div>
                        </div>
                        <span style={{ fontSize: '13px', color: '#64748b' }}>AI is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Quick Actions */}
              {showQuickActions && chatMessages.length === 0 && (
                <div className="ai-quick-actions">
                  <div className="ai-quick-actions-title">Try asking:</div>
                  <div className="ai-quick-actions-grid">
                    <button
                      onClick={() => handleQuickAction('study_plan')}
                      className="ai-quick-action-btn"
                    >
                      <Calendar size={14} />
                      Study Plan
                    </button>
                    <button
                      onClick={() => handleQuickAction('notes')}
                      className="ai-quick-action-btn"
                    >
                      <FileText size={14} />
                      Get Notes
                    </button>
                    
                  </div>
                </div>
              )}

              {/* Input Area */}
              <div className="ai-input-container">
                <div className="ai-input-wrapper">
                  <textarea
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                      }
                    }}
                    placeholder="Ask about study plans, notes ..."
                    className="ai-textarea"
                    rows={1}
                  />
                  <button 
                    onClick={sendMessage}
                    disabled={isLoading || !userInput.trim()}
                    className="ai-send-btn"
                  >
                    <Send size={16} />
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quiz Modal */}
        {showQuiz && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000
          }}>
            <div style={{
              backgroundColor: 'white',
              borderRadius: '8px',
              padding: '24px',
              width: '90%',
              maxWidth: '600px',
              maxHeight: '90vh',
              overflow: 'auto',
              position: 'relative'
            }}>
              <button 
                onClick={handleCloseQuiz}
                style={{
                  position: 'absolute',
                  top: '16px',
                  right: '16px',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                <X size={20} color="#6b7280" />
              </button>
              {!quizCompleted ? (
                <>
                  <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                    Question {currentQuestionIndex + 1} of {demoQuestions.length}
                  </h2>
                  <p style={{ fontSize: '18px', marginBottom: '24px', fontWeight: '500' }}>
                    {demoQuestions[currentQuestionIndex]?.question}
                  </p>
                  <div style={{ marginBottom: '24px' }}>
                    {demoQuestions[currentQuestionIndex]?.options.map((option, index) => (
                      <div 
                        key={index}
                        onClick={() => handleAnswerSelect(index)}
                        style={{
                          padding: '12px 16px',
                          border: `2px solid ${selectedAnswer === index ? '#0f766e' : '#e5e7eb'}`,
                          borderRadius: '8px',
                          marginBottom: '12px',
                          cursor: 'pointer',
                          backgroundColor: selectedAnswer === index ? '#f0fdfa' : 'white',
                          transition: 'all 0.2s'
                        }}
                      >
                        {option}
                      </div>
                    ))}
                  </div>
                  <button 
                    onClick={handleNextQuestion}
                    disabled={selectedAnswer === null}
                    style={{
                      width: '100%',
                      padding: '12px',
                      backgroundColor: selectedAnswer !== null ? '#0f766e' : '#9ca3af',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      fontSize: '16px',
                      fontWeight: '600',
                      cursor: selectedAnswer !== null ? 'pointer' : 'not-allowed'
                    }}
                  >
                    {currentQuestionIndex === demoQuestions.length - 1 ? 'Finish Quiz' : 'Next Question'}
                  </button>
                </>
              ) : (
                <>
                  <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '16px' }}>
                    Quiz Completed!
                  </h2>
                  <div style={{ 
                    textAlign: 'center', 
                    padding: '24px', 
                    backgroundColor: '#f0fdfa', 
                    borderRadius: '8px',
                    marginBottom: '24px'
                  }}>
                    <p style={{ fontSize: '18px', marginBottom: '8px' }}>
                      Your score: {quizScore} out of {demoQuestions.length}
                    </p>
                    <p style={{ fontSize: '16px', color: '#4b5563' }}>
                      {quizScore >= Math.ceil(demoQuestions.length * 0.8) 
                        ? 'Congratulations! You passed the quiz.' 
                        : 'Keep studying and try again.'}
                    </p>
                  </div>
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button 
                      onClick={handleCloseQuiz}
                      style={{
                        flex: 1,
                        padding: '12px',
                        backgroundColor: '#e5e7eb',
                        color: '#4b5563',
                        border: 'none',
                        borderRadius: '6px',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: 'pointer'
                      }}
                    >
                      Close
                    </button>
                    {remainingChances > 0 && quizScore < Math.ceil(demoQuestions.length * 0.8) && (
                      <button 
                        onClick={handleRetryQuiz}
                        style={{
                          flex: 1,
                          padding: '12px',
                          backgroundColor: '#0f766e',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '16px',
                          fontWeight: '600',
                          cursor: 'pointer'
                        }}
                      >
                        Try Again ({remainingChances} left)
                      </button>
                    )}
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default LessonPage;