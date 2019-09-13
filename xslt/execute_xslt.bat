java -jar c:/saxon/saxon9he.jar ../data/HANSARD-11-32902.xml HANSARD_General.xsl -o:output/xslt_HANSARD-11-32902_questions_and_answers.xml
java -jar c:/saxon/saxon9he.jar input/HANSARD-10-26906.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-26906_bill.xml
java -jar c:/saxon/saxon9he.jar input/HANSARD-10-27650.xml HANSARD_General.xsl -o:output/xslt_HANSARD-10-27650_question_time.xml

rem java -jar c:/saxon/saxon9he.jar input/HANSARD-10-27503.xml HANSARD_General.xsl -o:xsl_parliamentary_procedure.xml