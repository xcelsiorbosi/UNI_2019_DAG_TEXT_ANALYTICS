<?xml version='1.0' ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" />

	<xsl:template match="hansard">
		<xsl:element name="hansard">
			<xsl:element name="id"></xsl:element>
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
			<xsl:element name="url"></xsl:element>
			<xsl:element name="proceedingType"><xsl:value-of select="proceeding/name"/></xsl:element>
			<xsl:element name="subject"><xsl:value-of select="proceeding/subject/name"/></xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template match="talker">

	</xsl:template>

</xsl:stylesheet>
