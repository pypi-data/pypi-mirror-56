
def main():
    """Entry point for the application script"""
    print("Call your main application code here")

def countActiveWell(well,filter,condition):
    output_well = [x for x in well if (filter in x and x[filter] == condition )]
    # count all well retrieved from API
    print("total well count:" , len(well))
    # count well which is actived
    print("active well count:" , len(output_well))
    return output_well