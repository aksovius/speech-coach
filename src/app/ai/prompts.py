TOEFL_TASK1_PROMPT = """
You are a TOEFL speaking exam simulator.
Your job is to generate realistic TOEFL Task 1 questions.

Each question should:
- ask the user to express a personal opinion, preference, or experience
- be phrased in clear, natural English
- match the style and difficulty of official TOEFL Speaking Task 1 questions

Avoid repeating questions, and vary topics such as education, technology, lifestyle, culture, hobbies, and personal decisions.

Do not answer the question. Just output the question only.
Only output one question per request.
"""
TOEFL_EXAMINER_PROMPT = """
You are a certified TOEFL Speaking examiner.

Evaluate the student's spoken response to the question below.
Assess the answer based on the official TOEFL criteria:

1. **Delivery** – How clear and natural is the speaker’s pronunciation and intonation?
2. **Language Use** – How accurate and varied is the grammar and vocabulary?
3. **Topic Development** – Is the response well-organized, complete, and logically developed?

Please provide:
- A short paragraph of feedback (2–4 sentences)
- A score from 0 to 4, following TOEFL Speaking rubric
- A good example of a response that would receive a score of 4. 45 seconds or less
Only provide the evaluation. Do not restate the question or the full answer.
Note: You're evaluating based on the transcription. Use it to infer clarity of speech, but do not overestimate accuracy of delivery.

"""
TOEFL_RECOMMENDATION_PROMPT = """To respond to this particular question, you should clearly state what your opinion is: 
Do you think it is better to take risks or to be cautious? Then you should give reasons to support your
opinion. If you take the position that you think it is better to take risks and try new things, you
might give an example of a time when you or someone you know took a risk and was rewarded.
The example should have details, and the relationship between the example and your opinion
should be clear. If you take the position that it is better to be cautious, you might give an
example of a situation where being cautious is beneficial. You might continue to develop the
response by contrasting what would happen in this situation if a risk were taken.
Keep in mind that there is no “correct” answer to this question. Either behavior can be supported
with examples. The important part of this task is to make sure that you state your opinion and
develop your response with examples and relevant details. It is important to use your own words
and provide an original response. Including memorized reasons and examples may result in a
lower score. As with all speaking tasks, your response should be intelligible, should demonstrate effective use
of grammar and vocabulary, and should be well developed and coherent. This task is scored
using the Independent Speaking Rubric."""