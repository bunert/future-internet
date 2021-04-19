Describe your algorithm here
======
Our ABR algorithm is a hybrid algorithm which estimates the capacity observed between timeouts (200ms) and uses this in combination with a buffer based approach to increase/decrease the quality more aggressive if the buffer allows it. The algorithm also decides if it changes the current quality when a rebuffer event is triggered based on the number of bytes left of the current dowloading chunk.
