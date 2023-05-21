class Heap:
    def __init__(self,L):                  # create the heap
        self.data = L                      # data list is initialized
        self.pos = []                     
        for i in range(len(L)):
            self.pos.append(i)             # pos is an array storing the position of the tuple concerning the i'th and i+1'th object in the list 
        self.buildheap()                   # heap property satisfied after using buildheap

    def swap(self,a,b):                    # swaps the elements in the datalist
        self.data[a] , self.data[b] = self.data[b] , self.data[a]
        self.pos[self.data[a][1]] = a      # also update the pos array   
        self.pos[self.data[b][1]] = b      

    def heapup(self,x):                    
        while((x-1)//2 >= 0):
            if self.data[(x-1)//2] > self.data[x]:  # if the parent is larger,
                self.swap(x,(x-1)//2)      # swap the element with the parent 
                x = (x-1)//2
            else:
                return

    def heapdown(self,x):                  # while a child is smaller, swap element with its child
        while (2*x + 1 <= len(self.data) - 1):
            if (2*x + 1 == len(self.data) - 1):
                if self.data[2*x + 1] < self.data[x]:  
                    self.swap(x,2*x + 1)                  
                    x = 2*x + 1                           
                else:                                   
                    return                               
            else:                                        
                if self.data[2*x + 1] < self.data[2*x + 2] and self.data[2*x + 1] < self.data[x]:
                    self.swap(x,2*x+1)                      
                    x = 2*x + 1                         
                elif self.data[2*x + 2] < self.data[x]:
                    self.swap(x,2*x+2)                    
                    x = 2*x + 2                     
                else:                               
                    return       

    def extract_min(self):              # return the minimum element
        self.swap(0,-1)                 # swap the first and the last element 
        ans = self.data[-1]                
        self.data.pop()                 # remove the last element
        self.heapdown(0)                # move the first element down to its correct location     
        return ans
                                        
    def enque(self,x):                       
        self.data.append(x)                 # append the element to datalist
        self.heapup(len(self.data) - 1)     # move the last element up until needed
                                         
    def buildheap(self):                    # perform heap down on each element                 
        for i in range (len(self.data)-1 , -1 , -1):  # start from the end
            self.heapdown(i)                
                                               
    def updatekey(self,i,x):            # update an entry in the heap 
        if self.data[i] < x:            
            self.data[i] = x
            self.heapdown(i)            
        else:
            self.data[i] = x
            self.heapup(i)    

    def top(self):                      # return the minimum element,
        return self.data[0]             # without removing the element


def time_next_collision(i,x,v,last,T):  # function that returns the time of collision of the i and i+1 object
    if v[i] == v[i+1]:
        return T+1                      # time = T + 1 is never processed 
    t = ((x[i+1] - v[i+1]*last[i+1]) - (x[i] - v[i]*last[i]))/(v[i] - v[i+1]) # compute the collision time
    if t < last[i] or t < last[i+1]:    # if the collision time is not after the last collision 
        return T+1                      # the collision never happens
    else:                               # else store the correct time 
        return t


def listCollisions(M,x,v,m,T):
    n = len(M)                          # n = number of particles
    last = [0]*(n)                      # time of last collision of i'th particle
    ans = []                            # the list where we store the final answer
    L = []                              # L is a list of tuples (t,i),
    for i in range(n-1):                # where t is the time of next collision of i and i+1
        if v[i] == v[i+1]:               
            L.append((T+1,i))                          
        elif (x[i+1] - x[i])/(v[i] - v[i+1]) >= 0:                  
            L.append(((x[i+1] - x[i])/(v[i] - v[i+1]),i))                     
        else:
            L.append((T+1,i))
    h = Heap(L)                         # make L into a heap 
    for j in range(m): 
        (t,i) = h.top()                 # the next collision 
        if t>T:                         # if the next collision is after T, break the loop 
            break   
        x[i+1] , x[i] = x[i+1] + v[i+1]*(t - last[i+1]) , x[i] + v[i]*(t - last[i]) 
        v[i+1] , v[i] = (2*M[i]*v[i] - (M[i] - M[i+1])*v[i+1])/(M[i] + M[i+1]) , (2*M[i+1]*v[i+1] + (M[i] - M[i+1])*v[i])/(M[i] + M[i+1]) 
        last[i+1] , last[i] = t , t     # update velocities, positions, last collision times 
        ans.append((t,i,x[i]))
        h.updatekey(h.pos[i],(T+1,i))   # update the top entry of the heap 
        if i!=0:
            h.updatekey(h.pos[i-1],(time_next_collision(i-1,x,v,last,T),i-1))  # update collision time of i-1, i
        if i!=n-2 and i!=n-1:
            h.updatekey(h.pos[i+1],(time_next_collision(i+1,x,v,last,T),i+1))  # update collision time of i+1, i+2
        
    return ans
