rem Proceeding Types on Hansard as of 15/09/2019: http://hansardpublic.parliament.sa.gov.au/#/search/0
rem Question Time
java -jar saxon/saxon9he.jar input/HANSARD-10-27650.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-27650_question_time.xml

rem Answers to Questions
java -jar saxon/saxon9he.jar input/HANSARD-11-32902.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32902_questions_and_answers.xml

rem Bills
java -jar saxon/saxon9he.jar input/HANSARD-10-26906.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-26906_bill.xml

rem Estimate Replies
java -jar saxon/saxon9he.jar input/HANSARD-11-32917.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32917_estimate_replies.xml
java -jar saxon/saxon9he.jar input/HANSARD-11-32809.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32809_estimate_replies.xml

rem Parliamentary Procedure
java -jar saxon/saxon9he.jar input/HANSARD-10-27503.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-27503_parliamentary_procedure.xml

rem Grievance Debate
java -jar saxon/saxon9he.jar input/HANSARD-11-33467.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-33467_grievance_debate.xml

rem Motions
java -jar saxon/saxon9he.jar input/HANSARD-10-27074.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-27074_motions.xml

rem Parliamentary Committees
java -jar saxon/saxon9he.jar input/HANSARD-10-27076.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-27076_parliamentary_committees.xml

rem Commencement
java -jar saxon/saxon9he.jar input/HANSARD-10-25794.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-25794_commencement.xml

rem Matters of Interest
java -jar saxon/saxon9he.jar input/HANSARD-10-26007.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-26007_matters_interest.xml

rem Petitions
java -jar saxon/saxon9he.jar input/HANSARD-11-32830.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32830_petitions.xml

rem Estimate Vote
java -jar saxon/saxon9he.jar input/HANSARD-7-515.xml HANSARD_General.xsl -o:output/xslt_HANSARD-7-515_estimate_vote.xml

rem Ministerial Statement
java -jar saxon/saxon9he.jar input/HANSARD-10-26074.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-26074_ministerial_statement.xml

rem Personal Explanation
java -jar saxon/saxon9he.jar input/HANSARD-11-32867.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32867_personal_explanation.xml

rem Matter of Privilege
java -jar saxon/saxon9he.jar input/HANSARD-11-32827.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32827_matter_privilege.xml
