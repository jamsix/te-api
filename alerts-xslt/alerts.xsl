<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Alerts</h2>
  <table>
    <tr>
      <th style="text-align:left">Alert ID</th>
      <th style="text-align:left">Date Start</th>
      <th style="text-align:left">Scope</th>
      <th style="text-align:left">Test Name</th>
    </tr>
    <xsl:for-each select="teResults/alert">
    <tr>
      <td><xsl:value-of select="alertId" /></td>
      <td><xsl:value-of select="dateStart" /></td>
      <td><xsl:value-of select="violationCount" /></td>
      <td><xsl:value-of select="testName" /></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
