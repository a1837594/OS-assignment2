from mmu import MMU

#For randomly select
import random

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames
        self.page_table = {}
        self.frame_list = []

        #Counters
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0

        #For debug mode
        self.debug = False

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        self.access_memory(page_number, False)

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        self.access_memory(page_number, True)

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults
    
    #Method of Read and Write integrate into one function for their similarity in funcitonality
    def access_memory(self, page_number, is_write):
        #Check if the page is valid
        if page_number in self.page_table and self.page_table[page_number]['valid']:
            #Check if its for write_memory
            if is_write:
                self.page_table[page_number]['write'] = True
            #if debug mode is on
            if self.debug:
                print(f"Page {page_number} accessed in frame {self.page_table[page_number]['frame']}")
        #If the page is not valid / page fault occurs
        else:
            #Count times of page faults occured
            self.total_page_faults += 1
            #Report message in debug mode
            if self.debug:
                print(f"Page fault for page {page_number}")
            #Execute page_fault function
            self.page_fault(page_number, is_write)

    #Actions when page fault occured
    def page_fault(self, page_number, is_write):
        #If there's still a free frame available
        if len(self.frame_list) < self.frames:
            frame_number = len(self.frame_list)
            self.frame_list.append(page_number)
            if self.debug:
                print(f"Loading page {page_number} into frame {frame_number}")

        #Implement LRU when no free frame
        else:
            #Get the least recently used page
            rand_selected_page = self.rand_page()
            if self.debug:
                print(f"Replacing page {rand_selected_page} with page {page_number}")
            #if write_memory
            if self.page_table[rand_selected_page]['write']:
                self.total_disk_writes += 1
                if self.debug:
                    print(f"Writing page {rand_selected_page} to disk")
            frame_number = self.page_table[rand_selected_page]['frame']
            del self.page_table[rand_selected_page]
            self.frame_list[self.frame_list.index(rand_selected_page)] = page_number

        #Setup information
        self.page_table[page_number] = {
            'frame': frame_number,
            'valid': True,
            'write': is_write,
        }
        self.total_disk_reads += 1

    #Randomly select page
    def rand_page(self):
        index = random.randint(0, self.frames - 1)
        page = self.frame_list[index]
        return page