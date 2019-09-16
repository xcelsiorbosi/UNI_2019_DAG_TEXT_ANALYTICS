<?xml version='1.0' ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" />

	<xsl:template match="/">
        <xsl:element name="hansard">
		    <xsl:apply-templates select="hansard"/>
        </xsl:element>
   	</xsl:template>

	<xsl:template match="hansard">
		 <xsl:element name="header">
			<xsl:element name="name"><xsl:value-of select="name"/></xsl:element>
			<xsl:element name="parliamentName"><xsl:value-of select="parliamentName"/></xsl:element>
			<xsl:element name="parliamentNum"><xsl:value-of select="parliamentNum"/></xsl:element>
			<xsl:element name="reviewStage"><xsl:value-of select="reviewStage"/></xsl:element>
			<xsl:element name="sessionName"><xsl:value-of select="sessionName"/></xsl:element>
			<xsl:element name="sessionNum"><xsl:value-of select="sessionNum"/></xsl:element>
			<xsl:element name="venue"><xsl:value-of select="venue"/></xsl:element>
			<xsl:element name="date"><xsl:value-of select="date/@date"/></xsl:element>
			<xsl:element name="dateModified"><xsl:value-of select="dateModified/@time"/></xsl:element>
			<xsl:element name="house"><xsl:value-of select="house"/></xsl:element>
			<xsl:element name="proceedingType"><xsl:value-of select="proceeding/name"/></xsl:element>
			<xsl:element name="subject"><xsl:value-of select="proceeding/subject/name"/></xsl:element>
         </xsl:element>

        <xsl:apply-templates select="//bill" mode="bill"/>
		<xsl:apply-templates select="//*[not(self::talker)]/text" mode="proceeding"/> <!-- Include text that isn't speech -->
        <xsl:apply-templates select="//talker" mode="talker"/>

	</xsl:template>

	<xsl:template match="talker" mode="talker">
		<xsl:element name="talker">
			<xsl:element name="id"><xsl:value-of select="@id"/></xsl:element> <!-- TODO: need to handle case where a talker doesn't have an ID -->
			<xsl:element name="name"><xsl:value-of select="name"/></xsl:element>
			<xsl:element name="house"><xsl:value-of select="house"/></xsl:element>
			<xsl:element name="role"><xsl:value-of select="@role"/></xsl:element>
			<xsl:element name="electorate"><xsl:value-of select="electorate"/></xsl:element>
		</xsl:element>

		<xsl:apply-templates select=".//portfolio" mode="portfolio">
				<xsl:with-param name="talkerID" select="@id"/>
		</xsl:apply-templates>

		<xsl:apply-templates select=".//question" mode="question">
				<xsl:with-param name="talkerID" select="@id"/>
		</xsl:apply-templates>

		<xsl:apply-templates select=".//text" mode="text"/>
	</xsl:template>

	<xsl:template match="talker/text" mode="text">
		<xsl:element name="text">
			<xsl:element name="id"><xsl:value-of select="@id"/></xsl:element>
			<xsl:element name="talkerID"><xsl:value-of select="../@id"/></xsl:element>
			<xsl:element name="kind"><xsl:value-of select="../@kind"/></xsl:element>
			<xsl:element name="text">
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

		<xsl:element name="portfolio">
			<xsl:element name="talkerID">
				<xsl:value-of select="$talkerID"/>
			</xsl:element>
			<xsl:element name="id">
				<xsl:value-of select="@id"/>
			</xsl:element>
			<xsl:element name="name">
				<xsl:value-of select="name"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="bill" mode="bill">
		<xsl:element name="bill">
			<xsl:element name="id"><xsl:value-of select="@id"/></xsl:element>
			<xsl:element name="name"><xsl:value-of select="name"/></xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="question" mode="question">
		<xsl:param name="talkerID"/>

		<xsl:element name="question">
			<xsl:element name="talkerID">
				<xsl:value-of select="$talkerID"/>
			</xsl:element>
			<xsl:element name="date">
				<xsl:value-of select="@date"/>
			</xsl:element>
			<xsl:element name="qonNum">
				<xsl:value-of select="@qonNum"/>
			</xsl:element>
			<xsl:element name="name">
				<xsl:value-of select="name"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="text" mode="proceeding">
		<xsl:element name="proceedingText">
			<xsl:element name="id">
				<xsl:value-of select="@id"/>
			</xsl:element>
			<xsl:element name="text">
				<xsl:apply-templates select="* | text()"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>

</xsl:stylesheet>
