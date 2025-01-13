samples = """
"Hey! How’s your day going?" → true
"Did you have lunch already?" → true
"What are the latest trends in AI?" → false
"Got any plans for the weekend?" → true
"Can you explain convolutional neural networks?" → false
"The weather’s been nice lately, hasn’t it?" → true
"How do transformers work in NLP?" → false
"Did you see the movie everyone’s talking about?" → true
"What is your favorite holiday destination?" → true
"Define transfer learning in machine learning." → false
"I love your shoes! Where did you get them?" → true
"Can you summarize the key points of the paper?" → false
"How was your weekend?" → true
"What’s your favorite type of music?" → true
"How do generative models work?" → false
"Are you free later to grab a coffee?" → true
"What’s the difference between supervised and unsupervised learning?" → false
"Did you see the latest episode of that show?" → true
"Can you share the dataset you used for your experiment?" → false
"What’s your favorite food?" → true
"How was your trip?" → true
"What’s the methodology behind this research?" → false
"Did you try the new restaurant downtown?" → true
"Explain how attention mechanisms work." → false
"Do you like coffee or tea more?" → true
"Can you show me the experiment results?" → false
"It’s been a while! How have you been?" → true
"What are the common applications of deep learning?" → false
"Are you going to the party this weekend?" → true
"Can you explain backpropagation?" → false
"Did you hear about the new tech conference?" → true
"What’s your take on reinforcement learning?" → false
"I love your new haircut!" → true
"What datasets did you use in your analysis?" → false
"Any fun plans for the evening?" → true
"What’s the main challenge in your research?" → false
"Did you watch that new documentary?" → true
"How do recurrent neural networks differ from transformers?" → false
"How’s the family doing?" → true
"Can you elaborate on your findings?" → false
"It’s such a beautiful day, isn’t it?" → true
"What’s your favorite way to relax?" → true
"How does data augmentation improve model performance?" → false
"Have you seen the new art exhibit?" → true
"What preprocessing steps did you use?" → false
"Are you enjoying the book you’re reading?" → true
"Can you compare supervised and reinforcement learning?" → false
"Have you taken any good photos lately?" → true
"What’s your opinion on explainable AI?" → false
"Did you visit any cool places during your vacation?" → true
"Can you share your code implementation?" → false
"Are you excited for the weekend?" → true
"What’s the difference between precision and recall?" → false
"Do you prefer summer or winter?" → true
"How does regularization prevent overfitting?" → false
"Did you catch up with any old friends recently?" → true
"Can you summarize the literature review?" → false
"What’s your favorite TV show?" → true
"How do generative adversarial networks work?" → false
"What’s the best meal you’ve had recently?" → true
"Can you explain dropout in neural networks?" → false
"Do you enjoy hiking?" → true
"How is this approach different from traditional methods?" → false
"Did you attend the last team meeting?" → true
"What’s your go-to weekend activity?" → true
"What are the main metrics used for evaluation?" → false
"Have you been following any sports lately?" → true
"What’s the main contribution of this paper?" → false
"What’s your favorite holiday tradition?" → true
"Can you explain the gradient descent algorithm?" → false
"Are you free this weekend for a hangout?" → true
"How does batch normalization improve training?" → false
"Did you try that new dessert place?" → true
"What tools did you use for data visualization?" → false
"How do you usually spend your evenings?" → true
"Can you provide more details on the dataset?" → false
"How’s your morning been so far?" → true
"Can you explain unsupervised learning in simple terms?" → false
"What’s your favorite way to spend a lazy Sunday?" → true
"How do you evaluate model performance?" → false
"Any shows you’ve been binge-watching lately?" → true
"How does reinforcement learning work?" → false
"Do you enjoy traveling?" → true
"Can you explain the difference between L1 and L2 regularization?" → false
"Did you go to that new café everyone’s talking about?" → true
"What is your approach to feature selection?" → false
"Are you a morning or night person?" → true
"How do you handle missing data in your experiments?" → false
"Have you picked up any new hobbies lately?" → true
"Can you share the source of your research data?" → false
"Did you catch the sunset yesterday?" → true
"What’s the most interesting thing you’ve learned recently?" → true
"How does hyperparameter tuning improve performance?" → false
"Do you prefer working from home or at the office?" → true
"What are the limitations of your proposed method?" → false
"Have you tried cooking anything new?" → true
"Can you explain the architecture of the proposed model?" → false
"How’s everything going with your family?" → true
"What’s your preferred way of learning new skills?" → true
"What techniques did you use for model optimization?" → false
"""

chitchat_prompt = """
Given a question, determine if it's a typical conversation (chitchat) or a technical/academic question.
Questions about:
- Personal life, daily activities, preferences, hobbies
- Weather, food, entertainment, social activities
- Casual greetings and small talk
are considered chitchat (true).

Questions about:
- Technical concepts, algorithms, research
- Data science, machine learning, AI
- Implementation details, experiments, methodologies
are not chitchat (false).

Examples of chitchat:
{samples}
**RULES**
- Only return true or false
""".format(samples = samples)