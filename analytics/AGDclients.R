#loading requred library
library(readxl)
library(tidyr)
library(dplyr)
library(stringr)



#importing text sheet
Hansard1102019 = read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "Text")

#getting talker sheet
HANSARD.talker = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "Portfolio"))

#getting header sheet
HANSARD.header = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "Header"))

#getting HANSARDfilesinfo sheet
HANSARDFilesInfo = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "HANSARDFilesInfo"))

#getting talker names
Talkerstaging = data.frame(read_xlsx("C:\\Users\\Bipin Karki\\Downloads\\Hansard1102019.xlsx", sheet = "TalkerStaging"))


#Combining all the text transcript by HansardID, Kind and TalkerID
Hansard.Texts.all = Hansard1102019 %>% group_by(Kind, TalkerID, HansardID) %>% summarise(discussion = paste(Text, collapse = " "))

#merging talker information and header information
Hansard.Texts.all = merge(x = Hansard.Texts.all[,-c(1)], y = HANSARD.header[,-c(8,10)], 
                          by.x = c("HansardID"), by.y = c("HansardID"))

#merging talker information and file information
Hansard.Texts.all = data.frame(merge(x=Hansard.Texts.all, y=HANSARDFilesInfo[,-c(1,4)], 
                                     by.x = "HansardID", by.y = "FileName"))

#adding talker information on text with header info
Hansard.Texts.all$Name = HANSARD.talker[match(Hansard.Texts.all$TalkerID, 
                                              HANSARD.talker$TalkerID),"Name"]

#adding talker name
Hansard.Texts.all$TalkerName = Talkerstaging[match(Hansard.Texts.all$TalkerID, 
                                                   HANSARD.talker$TalkerID),"TalkerName"]

#changing date column in date format
Hansard.Texts.all$Date <- as.Date(Hansard.Texts.all$Date , "%y/%m/%d")


clientlist = list('Aboriginal Lands Trust', 'Adelaide and Mount Lofty Ranges Natural Resources Management Board',
                  'Adelaide Cemeteries Authority', 'Adelaide Dolphin Sanctuary Fund', 'Adelaide Festival Centre Trust', 'Adelaide Festival Corporation',
                  'Adelaide Film Festival', 'Adelaide Oval SMA Limited', 'Adelaide Venue Management Corporation', 'Agents Indemnity Fund',
                  'Alinytjara Wilurara Natural Resources Management Board', 'Art Gallery Board', "Attorney-General's Department", "Australian Children's Performing Arts Company",
                  'Australian Energy Market Commission', 'Board of the Botanic Gardens and State Herbarium', 'Carrick Hill Trust', 'Central Adelaide Local Health Network Incorporated',
                  'Child Protection - Department for', 'COAG Health Council', 'Coast Protection Board', 'Construction Industry Training Board',
                  'Correctional Services - Department for', 'Country Health SA Local Health Network Incorporated', 'Courts Administration Authority',
                  'CTP Insurance Regulator', 'Dairy Authority of South Australia', 'Defence SA', 'Distribution Lessor Corporation', 'Dog and Cat Management Board',
                  'Dog Fence Board', 'Education - Department for', 'Electoral Commission of South Australia', 'Electoral Districts Boundaries Commission',
                  'Electricity Industry Superannuation Scheme', 'Environment Protection Authority', 'Public sector agencies audited at 30 June 2018',
                  'Environment and Water - Department for', 'Essential Services Commission of South Australia', 'Eyre Peninsula Natural Resources Management Board',
                  'General Reserves Trust', 'Generation Lessor Corporation', "Governors' Pensions Scheme", 'Green Industries SA', 'Health and Wellbeing - Department for',
                  'Health Services Charitable Gifts Board', 'History Trust of South Australia', 'HomeStart Finance', 'Human Services - Department of',
                  'Independent Commissioner Against Corruption', 'Independent Gambling Authority', 'Independent Gaming Corporation Ltd', 'Investment Attraction South Australia',
                  "Judges' Pensions Scheme", 'Judicial Conduct Commissioner', 'Kangaroo Island Natural Resources Management Board', 'Legal Services Commission',
                  'Legislature - The - House of Assembly', 'Legislature - The - Joint Parliamentary Services', 'Legislature - The - Legislative Council',
                  'Libraries Board of South Australia', 'Lifetime Support Authority of South Australia', 'Local Government Finance Authority of South Australia',
                  'Lotteries Commission of South Australia', 'Maralinga Lands Unnamed Conservation Park Board', 'Medvet Science Pty Ltd',
                  'Minister for Primary Industries and Regional Development - Adelaide Hills Wine Industry Fund', 'Minister for Primary Industries and Regional Development - Barossa Wine Industry Fund',
                  'Minister for Primary Industries and Regional Development - Citrus Growers Fund', 'Minister for Primary Industries and Regional Development - Clare Valley Wine Industry Fund', 'Minister for Primary Industries and Regional Development - Eyre Peninsula Grain Growers Rail Fund',
                  'Minister for Primary Industries and Regional Development - Grain Industry Fund', 'Public sector agencies audited at 30 June 2018', 'Minister for Primary Industries and Regional Development - Grain Industry Research and Development Fund',
                  'Minister for Primary Industries and Regional Development - Langhorne Creek Wine Industry Fund','Minister for Primary Industries and Regional Development - McLaren Vale Wine Industry Fund', 'Minister for Primary Industries and Regional Development - Riverland Wine Industry Fund',
                  'Minister for Primary Industries and Regional Development - South Australian Apiary Industry Fund', 'Minister for Primary Industries and Regional Development - South Australian Cattle Industry Fund',
                  'Minister for Primary Industries and Regional Development - South Australian Grape Growers Industry Fund', 'Minister for Primary Industries and Regional Development - South Australian Pig Industry Fund',
                  'Minister for Primary Industries and Regional Development - South Australian Sheep Industry Fund', 'Motor Accident Commission', 'Museum Board', 'National Health Funding Pool - South Australian State Pool Account',
                  'National Landcare Program Single Holding Account (South Australia)', 'Native Vegetation Fund', 'Northern Adelaide Local Health Network Incorporated', 'Northern and Yorke Natural Resources Management Board',
                  'Office of the National Rail Safety Regulator', 'Outback Communities Authority', 'Parliamentary Budget Advisory Service', 'Parliamentary Superannuation Scheme',
                  'Planning and Development Fund', 'Planning, Transport and Infrastructure - Department of', 'Police Superannuation Scheme', 'Premier and Cabinet - Department of the',
                  'Primary Industries and Regions - Department of', 'Professional Standards Council', 'Public Trustee', 'Rail Commissioner', 'Residential Tenancies Fund', 'Retail Shop Leases Fund',
                  'Return to Work Corporation of South Australia', 'Riverbank Authority', 'Rural Industry Adjustment and Development Fund', 'SA Ambulance Service Inc',
                  'SA Metropolitan Fire Service Superannuation Scheme', 'SACE Board of South Australia', 'Public sector agencies audited at 30 June 2018', 'Second-hand Vehicles Compensation Fund',
                  'Small Business Commissioner', 'South Australia Police', 'South Australian Ambulance Service Superannuation Scheme', 'South Australian Arid Lands Natural Resources Management Board', 'South Australian Country Arts Trust', 'South Australian Country Fire Service',
                  'South Australian Film Corporation', 'South Australian Fire and Emergency Services Commission', 'South Australian Forestry Corporation', 'South Australian Government Financing Authority',
                  'South Australian Housing Trust', 'South Australian Local Government Grants Commission', 'South Australian Mental Health Commission', 'South Australian Metropolitan Fire Service', 'South Australian Murray-Darling Basin Natural Resources Management Board',
                  'South Australian State Emergency Service', 'South Australian Superannuation Board', 'South Australian Superannuation Scheme', 'South Australian Tourism Commission', 'South Australian Water Corporation', 'South Australian Water Corporation - Hydro Joint Venture',
                  'South East Natural Resources Management Board', 'South Eastern Water Conservation and Drainage Board', 'Southern Adelaide Local Health Network Incorporated', 'Southern State Superannuation Scheme',
                  'State Development - Department of', 'State Opera of South Australia', 'State Planning Commission', 'State Procurement Board', 'State Theatre Company of South Australia', 'Stormwater Management Authority',
                  'StudyAdelaide', 'Super SA Retirement Investment Fund', 'Super SA Select Fund', 'Public sector agencies audited at 30 June 2018', 'Superannuation Funds Management Corporation of South Australia',
                  'TAFE SA', 'Teachers Registration Board of South Australia', 'TechInSA', 'The Flinders University of South Australia', 'Transmission Lessor Corporation', 'Department of Treasury and Finance',
                  'University of Adelaide', 'University of South Australia', 'Urban Renewal Authority', 'West Beach Trust', "Women's and Children's Health Network Incorporated", 'StateNet', 'ISMF', 'CHRIS 21', 'CommBiz', 'Masterpiece', 'Basware', 'Oracle', 'Findur',
                  'Bluedoor', 'Quantum', 'MAC', 'PROMIS', 'Grants management system', 'Ellipse', 'Empower', 'BDM', 'Student2', 'Enterprise system',
                  'EMR', 'EPAS', 'CHIRON', 'EPLIS', 'ECMS', 'End user computing', 'EMS', 'TRUMPS', 'FARMS', 'FAMIS', 'SA Housing BST',
                  'TechOne', 'Aon Risk Console', 'Curram', 'SAILIS', 'Distributing Computer Support Services', 'Alexandrina Council', 'The Barossa Council', 'Barunga West Council', 'Berri Barmera Council',
                  'City of Burnside', 'Campbelltown City Council', 'District Council of Ceduna', 'City of Charles Sturt', 'Clare & Gilbert Valleys Council',
                  'District Council of Cleve', 'District Council of Coober Pedy', 'Coorong District Council', 'Copper Coast Council', 'District Council of Elliston',
                  'The Flinders Ranges Council', 'District Council of Franklin Harbour', 'Town of Gawler', 'Regional Council of Goyder',
                  'District Council of Grant', 'City of Holdfast Bay', 'Kangaroo Island Council', 'District Council of Karoonda East Murray',
                  'District Council of Kimba', 'Kingston District Council', 'Light Regional Council', 'District Council of Lower Eyre Peninsula',
                  'District Council of Loxton Waikerie', 'City of Marion', 'Mid Murray Council', 'City of Mitcham', 'Mount Barker District Council',
                  'City of Mount Gambier', 'District Council of Mount Remarkable', 'The Rural City of Murray Bridge', 'Naracoorte Lucindale Council',
                  'Northern Areas Council', 'City of Norwood Payneham & St Peters', 'City of Onkaparinga', 'District Council of Orroroo Carrieton',
                  'District Council of Peterborough', 'City of Playford', 'City of Port Adelaide Enfield', 'Port Augusta City Council',
                  'City of Port Lincoln', 'Port Pirie Regional Council', 'City of Prospect', 'Renmark Paringa Council', 'District Council of Robe',
                  'Municipal Council of Roxby Downs', 'City of Salisbury', 'Southern Mallee District Council', 'District Council of Streaky Bay',
                  'Tatiara District Council', 'City of Tea Tree Gully', 'District Council of Tumby Bay', 'City of Unley', 'City of Victor Harbor',
                  'Wakefield Regional Council', 'Corporation of the Town of Walkerville', 'Wattle Range Council', 'City of West Torrens',
                  'City of Whyalla', 'Wudinna District Council', 'District Council of Yankalilla', 'Yorke Peninsula Council', 'Local Government Association (LGA)',
                  'Office of Local Government')


#here header is the dataframe where we need to search for client name
# discussion is the texts from which column cleint name is to be searched
dataframe_list <- lapply(clientlist, function(clientName) {
  Hansard.Texts.all %>% filter(str_detect(discussion, regex(clientName))) 
})

#assigning client name to the dataframe
names(dataframe_list) <- clientlist

#flat file with client name
library(plyr)
Client_File <- ldply(dataframe_list, data.frame)
detach(package:plyr)

write.csv(Client_File, "Client_File.csv")

