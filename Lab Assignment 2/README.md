Lab Group # 19

Group Members

Muhammad Hamza Khan Afridi 30257557

Muhammad Sajjad 30234125

Muhammad Saqib 30265504

Zain Aabaideen 30270057

Lab Assignment Summary:

Part 1 is basically about figuring out where a GPS receiver is located using the distances it measures from several satellites. 
To do this, we use two methods,Least Squares and Gradient Descent, in which both start with an initial guess and then keep adjusting it
until the predicted distances match the real ones. In this part, we set up the math (like the design matrix), run the iterations, and 
check how well the solutions converge.


Part 2 focuses on predicting student depression using logistic regression. The dataset is explored by checking class distribution and 
creating both full and smaller subsets for testing. Logistic regression is trained on different versions of the data, and its performance 
is evaluated using accuracy, log loss, confusion matrices, and classification reports. Additional models such as Naive Bayes and KNN are 
also compared to see how they perform on the same prediction task.


Part 3 focuses on classifying handwritten digits from the MNIST dataset using two different neural network models: an MLP and a CNN. 
The dataset is loaded, visualized, and preprocessed, and then both models are built and trained. The MLP treats each pixel as a separate 
feature, while the CNN learns spatial patterns like edges and curves. After training, both models are evaluated and compared using accuracy 
scores, training curves, and prediction examples. Overall, this part highlights why CNNs are more effective for image data and how their 
ability to capture visual structure leads to better performance.