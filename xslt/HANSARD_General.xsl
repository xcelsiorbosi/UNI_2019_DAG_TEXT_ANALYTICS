<?xml version='1.0' ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" />

	<xsl:template match="/">
        <xsl:element name="hansard">
		    <xsl:apply-templates select="hansard"/>
        </xsl:element>
   	</xsl:template>

	<xsl:template match="hansard">
		 <xsl:element name="Header">
			 <xsl:element name="HansardID">filename_generated_id</xsl:element>
			 <xsl:element name="Name"><xsl:value-of select="name"/></xsl:element>
			 <xsl:element name="ParliamentName"><xsl:value-of select="parliamentName"/></xsl:element>
		 	 <xsl:element name="ParliamentNum"><xsl:value-of select="parliamentNum"/></xsl:element>
		 	 <xsl:element name="ReviewStage"><xsl:value-of select="reviewStage"/></xsl:element>
			 <xsl:element name="SessionName"><xsl:value-of select="sessionName"/></xsl:element>
			 <xsl:element name="SessionNum"><xsl:value-of select="sessionNum"/></xsl:element>
			 <xsl:element name="Venue"><xsl:value-of select="venue"/></xsl:element>
			 <xsl:element name="Date"><xsl:value-of select="date/@date"/></xsl:element>
			 <xsl:element name="DateModified"><xsl:value-of select="dateModified/@time"/></xsl:element>
			 <xsl:element name="House"><xsl:value-of select="house"/></xsl:element>
			 <xsl:element name="URL">generated_url</xsl:element>
			 <xsl:element name="ProceedingType"><xsl:value-of select="proceeding/name"/></xsl:element>
			 <xsl:element name="Subject"><xsl:value-of select="proceeding/subject/name"/></xsl:element>
         </xsl:element>

        <xsl:apply-templates select="//bill" mode="bill"/>
		<xsl:apply-templates select="//*[not(self::talker)]/text" mode="proceeding"/> <!-- Include text that isn't speech -->
        <xsl:apply-templates select="//talker" mode="talker"/>

	</xsl:template>

	<xsl:template match="talker" mode="talker">

		<xsl:variable name="talkerID">
			<xsl:choose>
				<xsl:when test="@id != ''">
					<xsl:value-of select="@id" />
				</xsl:when>
				<xsl:otherwise>
					<!-- Generate talker ID if it does not exist -->
					<xsl:value-of select="generate-id(.)" />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:element name="Talker">
			<xsl:element name="TalkerID"><xsl:value-of select="$talkerID"/></xsl:element>
			<xsl:element name="Name"><xsl:value-of select="name"/></xsl:element>
			<xsl:element name="House"><xsl:value-of select="house"/></xsl:element>
			<xsl:element name="Role"><xsl:value-of select="@role"/></xsl:element>
			<xsl:element name="Electorate"><xsl:value-of select="electorate"/></xsl:element>
		</xsl:element>

		<xsl:apply-templates select=".//portfolio" mode="portfolio">
				<xsl:with-param name="talkerID" select="$talkerID"/>
		</xsl:apply-templates>

		<xsl:apply-templates select=".//question" mode="question">
				<xsl:with-param name="talkerID" select="$talkerID"/>
		</xsl:apply-templates>

		<xsl:apply-templates select=".//text" mode="text">
			<xsl:with-param name="talkerID" select="$talkerID"/>
		</xsl:apply-templates>
	</xsl:template>

	<xsl:template match="talker/text" mode="text">
		<xsl:param name="talkerID"/>

		<xsl:element name="Text">
			<xsl:element name="TextID"><xsl:value-of select="@id"/></xsl:element>
			<xsl:element name="TalkerID"><xsl:value-of select="$talkerID"/></xsl:element>
			<xsl:element name="HansardID">filename_generated_id</xsl:element>
			<xsl:element name="Kind"><xsl:value-of select="../@kind"/></xsl:element>
			<xsl:element name="Text">
				<xsl:apply-templates select="* | text()"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="by" mode="by">
		<xsl:value-of select="./text()"/> <!-- Text inside 'by' element -->
	</xsl:template>

	<xsl:template match="inserted" mode="inserted">
		<xsl:value-of select="./text()"/> <!-- Text inside 'inserted' element -->
	</xsl:template>

	<xsl:template match="item" mode="item">
		<xsl:value-of select="./text()"/> <!-- Text inside 'item' element -->
	</xsl:template>

	<xsl:template match="term" mode="term">
		<xsl:value-of select="./text()"/> <!-- Text inside 'term' element -->
	</xsl:template>

	<xsl:template match="text()">
		<xsl:value-of select="." />
   	</xsl:template>

	<xsl:template match="portfolio" mode="portfolio">
		<xsl:param name="talkerID"/>

		<xsl:element name="Portfolio">
			<xsl:element name="PortfolioID">generated_id</xsl:element>
			<xsl:element name="TalkerID">
				<xsl:value-of select="$talkerID"/>
			</xsl:element>
			<xsl:element name="Name">
				<xsl:value-of select="name"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="bill" mode="bill">
		<xsl:variable name="billID">
			<xsl:choose>
				<xsl:when test="@id != ''">
					<xsl:value-of select="@id" />
				</xsl:when>
				<xsl:otherwise>
					<!-- Generate Bill ID if it does not exist -->
					<xsl:value-of select="generate-id(.)" />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:element name="Bill">
			<xsl:element name="BillID"><xsl:value-of select="$billID"/></xsl:element>
			<xsl:element name="HansardID">filename_generated_id</xsl:element>
			<xsl:element name="BillName"><xsl:value-of select="name"/></xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="question" mode="question">
		<xsl:param name="talkerID"/>

		<xsl:element name="Question">
			<xsl:element name="QuestionID">generated_id</xsl:element>
			<xsl:element name="TalkerID">
				<xsl:value-of select="$talkerID"/>
			</xsl:element>
			<xsl:element name="HansardID">filename_generated_id</xsl:element>
			<xsl:element name="Date">
				<xsl:value-of select="@date"/>
			</xsl:element>
			<xsl:element name="QonNum">
				<xsl:value-of select="@qonNum"/>
			</xsl:element>
			<xsl:element name="Question">
				<xsl:value-of select="name"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="text" mode="proceeding">
		<xsl:element name="Text">
			<xsl:element name="TextID"><xsl:value-of select="@id"/></xsl:element>
			<xsl:element name="TalkerID"/>
			<xsl:element name="HansardID">filename_generated_id</xsl:element>
			<xsl:element name="Kind">proceeding</xsl:element>
			<xsl:element name="Text">
				<xsl:apply-templates select="* | text()"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

</xsl:stylesheet>
