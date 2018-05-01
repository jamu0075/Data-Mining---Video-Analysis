# Real-Time Video Analysis  

## Contributors: Akash, Jacob, Avery  

### Description:  
Our goal for this project was to see if we could modify a real-time object recognition algorithm (Darkflow/Tensorflow) 
to predict the next location of an object. We used a collection of ~14 million images to 'teach' the
algorithm to recognize the most common objects in day to day life. Our other goal, and potentially more impactful, was to 
find a way to more reliably test object detection algorithms. If you are able to easily test for marginal improvements it
becomes much easier to advance your algorithm.

### Questions:  
1. How can we test our algorithm for improvements?
    * We want to be able to check for slight speed improvements on our algorithm so we mined YouTube videos to get clips. These clips are then distributed based on their frame differnces which allowed us to sample for a desired amount of movement.
    clips of a desired speed. As improvements are made you can easily sample from slightly faster clips.
1. Is it even possible?  
    * Can we actually predict the next location using machine learning tools.  
2. What is the benefit?  
    * By being able to predict the next location of an object we can significantly reduce the processing time of  
    real-time video object recognition. Rather than scanning every frame, the algorithm could scan every other frame and predict
    in between, instantly doubling the speed. Or every 3rd frame, tripling the speed. The goal is to increase the gap until the prediction     becomes inaccurate.
3. Why?
    * Currently object recognition is either really accurate and really slow or really fast and not so accurate. 
    We want a really fast and really accurate object recognition tool for real-time use. If object recognition is fast and  
    accurate in real time video the applications are essentially endless.  
    
### Applications:  
By using our method of mining YouTube videos anyone is able to easily find a desired clip to test object detection. This method of sampling clips from a distribution Having a fast and accurate real-time object detection algorithm could allow cameras to constantly, and accurately,
search for threats in public spaces. It could also be used to assist blind people by conveying their surrondings through audio.
As mentioned before, the applications are essentially limitless.  

### Video Demonstration:  
*Link Here*  

### Final Paper:  
*Link Here*

