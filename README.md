**Project Name:** LLM Plan Optimizer

**Overview:**
The LLM Plan Optimizer is a web-based interface that enables users to select two Large Language Models (LLMs) to collaborate on creating a plan. One LLM is designated as the evaluator, while the other is the optimizer. The optimizer creates a plan based on a given prompt, and the evaluator provides feedback in the form of comments. The optimizer then revises the plan based on the feedback, and the process is repeated until both parties are satisfied. The final plan is presented to the user, along with an option to view the details of each step in the optimization process.

**Features:**

1. **LLM Selection:** A user-friendly interface to list and select multiple LLMs.
2. **Evaluator and Optimizer Selection:** Mark one LLM as the evaluator and the other as the optimizer.
3. **Prompt Input:** Provide a prompt for the optimizer to create a plan.
4. **Plan Evaluation:** The evaluator reviews the plan and provides comments.
5. **Plan Revision:** The optimizer revises the plan based on the feedback.
6. **Iteration:** Repeat the evaluation and revision process until both parties are satisfied.
7. **Plan Presentation:** Present the final plan to the user.
8. **Step-by-Step Details:** View the details of each step in the optimization process.

**Technical Requirements:**

* Python 3.8 or higher
* Flask or Django web framework
* LLM APIs (e.g., Hugging Face Transformers)
* Front-end framework (e.g., React, Angular, Vue.js)

**Getting Started:**

1. Clone the repository and install the required dependencies.
2. Set up the LLM APIs and configure the interface to connect to the APIs.
3. Run the application and access it through a web browser.
    - docker build -t evaluator_app .
    - docker run -p 8000:8000 evaluator_app
4. Follow the prompts to select LLMs, provide a prompt, and iterate through the optimization process.

**Future Development:**

* Integrate additional LLMs and APIs
* Implement more advanced optimization techniques
* Enhance the user interface and user experience
* Add support for multiple prompts and plans

**Contributing:**

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request with your changes.
