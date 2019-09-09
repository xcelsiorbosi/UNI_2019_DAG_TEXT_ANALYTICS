<?xml version='1.0' ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" version="1.0" encoding="UTF-8" />
      <xsl:template match="/">
            <xsl:element name="hansard">
				<xsl:element name="header">
					<xsl:element name="name">
						<xsl:value-of select="hansard/name"/>
					</xsl:element>
					<xsl:element name="date">
						<xsl:value-of select="hansard/date/@date"/>
					</xsl:element>
					<xsl:element name="sessionName">
						<xsl:value-of select="hansard/sessionName"/>
					</xsl:element>
					<xsl:element name="parliamentNum">
						<xsl:value-of select="hansard/parliamentNum"/>
					</xsl:element>
					<xsl:element name="sessionNum">
						<xsl:value-of select="hansard/sessionNum"/>
					</xsl:element>
					<xsl:element name="parliamentName">
						<xsl:value-of select="hansard/parliamentName"/>
					</xsl:element>
					<xsl:element name="reviewStage">
						<xsl:value-of select="hansard/reviewStage"/>
					</xsl:element>
					<xsl:element name="dateModified">
						<xsl:value-of select="hansard/dateModified/@time"/>
					</xsl:element>
					<xsl:element name="proceeding">
						<xsl:value-of select="hansard/proceeding/@continued"/>
					</xsl:element>
					<xsl:element name="name">
						<xsl:value-of select="hansard/proceeding/name"/>
					</xsl:element>
				</xsl:element>

				<xsl:for-each select="hansard/proceeding/subject">
					<xsl:element name="question">
						<xsl:element name="qTextID">
							<xsl:value-of select="./text/@id"/>
						</xsl:element>
						<xsl:element name="qHeading">
							<xsl:value-of select="./text/inserted/heading"/>
						</xsl:element>
						<xsl:element name="talkerID">
							<xsl:value-of select="./talker/@id"/>
						</xsl:element>
						<xsl:element name="talkKind">
							<xsl:value-of select="./talker/@kind"/>
						</xsl:element>
						<xsl:element name="qDate">
							<xsl:value-of select="./talker/questions/question/@date"/>
						</xsl:element>
						<xsl:element name="qNum">
							<xsl:value-of select="./talker/questions/question/@qonNum"/>
						</xsl:element>
					</xsl:element>
				</xsl:for-each>						
				<xsl:for-each select="hansard/proceeding/subject/talker/text">
					<xsl:element name="text">
						<xsl:element name="textID">
							<xsl:value-of select="./@id"/>
						</xsl:element>
						<xsl:element name="talkerID">
							<xsl:choose>
								<xsl:when test="./inserted/by/@id != ''">
									<xsl:number value="./inserted/by/@id" />
								</xsl:when>
								<xsl:otherwise>
									<xsl:number value="../@id" />
								</xsl:otherwise>
							</xsl:choose>
						</xsl:element>
						<xsl:element name="talkerRole">
							<xsl:value-of select="../@role"/>
						</xsl:element>
						<xsl:element name="talkKind">
							<xsl:value-of select="../@kind"/>
						</xsl:element>
						<xsl:element name="talkerName">
							<xsl:value-of select="../name"/>
						</xsl:element>
						<xsl:element name="talkerTranscript">
							<xsl:choose>
								<xsl:when test="./inserted/by/@id != ''">
									<xsl:value-of select="./inserted/text()[not(child::text())]"/>
									<xsl:value-of select="./inserted/text()[last()]"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="./inserted/text()"/>
								</xsl:otherwise>
							</xsl:choose>							
						</xsl:element>
					</xsl:element>
				</xsl:for-each>				
		  </xsl:element>
	  </xsl:template>
  </xsl:stylesheet>
