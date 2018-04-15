# Real-Time Video Analysis  

## Contributors: Akash, Jacob, Avery  

### Description:  
Our goal for this project was to see if we could modify a real-time object recognition algorithm (Darkflow/Tensorflow) 
to predict the next location of an object. We used this algorithm and a collection of ~14 million images to 'teach' the
algorithm to recognize the most common objects in day to day life. A simple inital boost in speed was to scan the video every 30 frames
rather than every frame, providing and instant 30x increase in speed. The bulk of the project is teaching the algorithm how objects
move in a frame.

### Questions:  
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
Having a fast and accurate real-time object detection algorithm could allow cameras to constantly, and accurately,
search for threats in public spaces. It could also be used to assist blind people by conveying their surrondings through audio.
As mentioned before, the applications are essentially limitless.  

### Video Demonstration:  
*Link Here*  

### Final Paper:  
*Link Here*

