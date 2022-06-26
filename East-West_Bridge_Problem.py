from threading import Lock,Thread
import logging
import time
import random

class Bridge:
    
        def __init__(self,min_cars,max_cars,t_min,t_max,max_cars_on_bridge):
            #initialize the directions of the cars
            self.directions = ['Right','Left']
            #Initialize the minimum and maximum amount of possible cars
            self.min_cars = min_cars
            self.max_cars = max_cars
            #Initialize the minimum and maximum durations
            #for a car to Cross the bridge.
            self.t_min = t_min
            self.t_max = t_max
            #Initialize the  Threads List(cars).
            self.cars = []
            self.car_directions = []
            self.car_crossing_times = []
            #Initialize a random amount of Threads 
            #Create a random list of directions thet the cars begin with.
            self.cars_num = random.randint(self.min_cars,self.max_cars)
            for i in range(self.cars_num):
                self.car_directions.append(random.choice(self.directions))
                self.car_crossing_times.append(random.randint(self.t_min,self.t_max))
            log_format = "%(asctime)s %(message)s"
            logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S ")
            #Assign the maximum amount of cars on the bridge.
            self.max_cars_on_bridge = max_cars_on_bridge
            #Inilialize the Left Lock (referring to arrive_bridge).
            self.left_dir_lock = Lock()
            self.left_dir_counter = 0
            #Inilialize the Right Lock (referring to arrive_bridge).
            self.right_dir_lock = Lock()
            self.right_direction_counter = 0       
            #Initialize the lock variable for the maximum amount of cars on the bridge.
            self.cars_on_bridge_lock = Lock()
            self.cars_on_bridge = 0
            #Initialize the lock variable to prohibit cars crossing the bridge from opposite directions.
            self.right_crossing_lock = Lock()
            self.left_crossing_lock = Lock()
            #Initialize lock variable to maintain the priority of the cars.
            self.service_lock = Lock()
        
            
        
        
        def arrive_bridge(self, car_No, car_dir):
            logging.info('Car {:d} with direction {:s} arrived at the bridge\n'.format(car_No,car_dir))
            if car_dir == 'Left':
                with self.left_dir_lock:
                    self.left_dir_counter += 1
            else:
                with self.right_dir_lock:
                    self.right_direction_counter += 1
            
                    
        
        def cross_bridge(self,car_No,car_dir,car_crossing_time):       
                if car_dir == 'Left':
                    with self.left_dir_lock:
                            self.left_dir_counter -= 1
                    with self.service_lock:
                        with self.left_crossing_lock:                      
                             with self.cars_on_bridge_lock:  
                                self.cars_on_bridge +=1  
                                if self.cars_on_bridge == 1:
                                    self.right_crossing_lock.acquire()
                             if self.cars_on_bridge == 3:
                                    self.cars_on_bridge_lock.acquire()
                else:
                    with self.right_dir_lock:
                            self.right_direction_counter -= 1
                    with self.service_lock: 
                        with self.right_crossing_lock:                        
                            with self.cars_on_bridge_lock:      
                                self.cars_on_bridge +=1  
                                if self.cars_on_bridge == 1:
                                    self.left_crossing_lock.acquire()
                            if self.cars_on_bridge == 3:
                                    self.cars_on_bridge_lock.acquire()             
                logging.info('Car {:d} with direction {:s} is crossing the bridge for {:d} seconds \n'.format(car_No,car_dir,car_crossing_time))
                time.sleep(car_crossing_time)
                
            
        
        def exit_bridge(self, car_No, car_dir):
            if self.cars_on_bridge ==3 :
                if car_dir == 'Left':
                            self.cars_on_bridge -=1 
                            if self.cars_on_bridge == 0:
                                self.right_crossing_lock.release()
                else:    
                            self.cars_on_bridge -=1  
                            if self.cars_on_bridge == 0:
                                self.left_crossing_lock.release()
                self.cars_on_bridge_lock.release()            
            else:             
                if car_dir == 'Left':
                        with self.cars_on_bridge_lock:
                            self.cars_on_bridge -=1   
                            if self.cars_on_bridge == 0:
                                self.right_crossing_lock.release()
                else:
                        with self.cars_on_bridge_lock:
                            self.cars_on_bridge -=1  
                            if self.cars_on_bridge == 0:
                                self.left_crossing_lock.release()
            logging.info('Car {:d} with direction {:s} is exiting the bridge\n'.format(car_No, car_dir))
            
            
        
        def car(self,car_No,car_dir,car_crossing_time):
            while True:
                #In case we wanted for each car being created from each thread to have random directions we should add
                #the following lines of code.
                #directio = ['Right','Left']
                #car_dir= random.choice(directio)

                t_arrive = random.randint(self.t_min,self.t_max)
                logging.info('Car {:d} with direction {:s} begins to move, {:d}s until it reaches the bridge\n'.format(car_No,car_dir,t_arrive))              
                time.sleep(t_arrive)
                self.arrive_bridge(car_No, car_dir)
                self.cross_bridge(car_No,car_dir, car_crossing_time)
                self.exit_bridge(car_No, car_dir)
                
                
        def create_threads(self):
           for car_No in range(0,self.cars_num):
               thread = Thread(target=self.car, args=(car_No+1,self.car_directions[car_No],self.car_crossing_times[car_No],))
               self.cars.append(thread)
               self.cars[-1].start()
               
               
        
        def join_threads(self):
            for thread in self.cars:
                thread.join()
                
                
def main():
    min_cars = 4
    max_cars = 9
    max_cars_on_bridge = 3
    t_min = 5
    t_max = 10
    bridge_sim = Bridge(min_cars,max_cars,t_min,t_max,max_cars_on_bridge)
    bridge_sim.create_threads()
    bridge_sim.join_threads()
    print("Finished.")
    
    
    
    
    
if __name__ == '__main__':
    main()
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                

