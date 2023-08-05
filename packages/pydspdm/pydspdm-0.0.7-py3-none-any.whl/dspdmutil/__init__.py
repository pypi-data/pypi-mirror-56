
def main():
    """Entry point for the application script"""
    print("Call your main application code here")

def countActiveWell(well):
    output_well = [x for x in well if ("ACTIVE_IND" in x and x["ACTIVE_IND"] == True )]
    # count all well retrieved from API
    print("total well count:" , len(well))
    # count well which is actived
    print("active well count:" , len(output_well))
    return output_well