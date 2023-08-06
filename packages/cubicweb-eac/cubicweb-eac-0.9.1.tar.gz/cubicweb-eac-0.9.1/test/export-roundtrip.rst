A roundtrip export test case
============================

.. code-block:: python

    >>> from __future__ import print_function
    >>> from six import text_type
    >>> fpath = self.datapath('FRAD033_EAC_00001_simplified_export.xml')
    >>> created, updated = testutils.eac_import(cnx, fpath)
    >>> record = cnx.find('AuthorityRecord', isni=u'22330001300016').one()
    >>> generated_eac = record.cw_adapt_to('EAC-CPF').dump(_encoding=text_type)
    >>> print(generated_eac)
    <?xml version='1.0'?>
    <eac-cpf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="urn:isbn:1-931666-33-4" xsi:schemaLocation="urn:isbn:1-931666-33-4 http://eac.staatsbibliothek-berlin.de/schema/cpf.xsd">
      <control>
        <recordId>987654321</recordId>
        <otherRecordId>1234</otherRecordId>
        <otherRecordId localType="letters">ABCD</otherRecordId>
        <maintenanceStatus>revised</maintenanceStatus>
        <publicationStatus>inProcess</publicationStatus>
        <maintenanceAgency>
          <agencyName/>
        </maintenanceAgency>
        <languageDeclaration>
          <language languageCode="fre">français</language>
          <script scriptCode="Latn">latin</script>
        </languageDeclaration>
        <maintenanceHistory>
          <maintenanceEvent>
            <eventType>revised</eventType>
            <eventDateTime standardDateTime="2015-01-15T07:16:33">2015-01-15T07:16:33</eventDateTime>
            <agentType>human</agentType>
            <agent>Delphine Jamet</agent>
          </maintenanceEvent>
          <maintenanceEvent>
            <eventType>created</eventType>
            <eventDateTime standardDateTime="2013-04-24T05:34:41">2013-04-24T05:34:41</eventDateTime>
            <agentType>machine</agentType>
            <agent/>
            <eventDescription>bla bla bla</eventDescription>
          </maintenanceEvent>
        </maintenanceHistory>
        <sources>
          <source>
            <sourceEntry>1. Ouvrages imprimés...</sourceEntry>
            <descriptiveNote>
              <p>des bouquins</p>
            </descriptiveNote>
          </source>
          <source xlink:href="http://archives.gironde.fr" xlink:type="simple">
            <sourceEntry>Site des Archives départementales de la Gironde</sourceEntry>
            <objectXMLWrap>
              <some>thing</some>
            </objectXMLWrap>
          </source>
        </sources>
      </control>
      <cpfDescription>
        <identity>
          <entityId>22330001300016</entityId>
          <entityType>corporateBody</entityType>
          <nameEntry>
            <part>Gironde. Conseil général</part>
          </nameEntry>
        </identity>
        <description>
          <existDates>
            <dateRange>
              <fromDate standardDate="1800-01-01">1800-01-01</fromDate>
              <toDate standardDate="2099-01-01">2099-01-01</toDate>
            </dateRange>
          </existDates>
          <places>
            <place>
              <placeRole>dodo</placeRole>
              <placeEntry>Lit</placeEntry>
            </place>
            <place>
              <placeRole>domicile</placeRole>
              <placeEntry longitude="1.44367" latitude="43.60426" localType="other">Toulouse (France)</placeEntry>
            </place>
            <place>
              <placeRole>siege</placeRole>
              <placeEntry vocabularySource="http://catalogue.bnf.fr/ark:/12148/cb152418385">Bordeaux (Gironde, France)</placeEntry>
              <address>
                <addressLine localType="StreetName">1 Esplanade Charles de Gaulle</addressLine>
                <addressLine localType="PostCode">33074</addressLine>
                <addressLine localType="CityName"> Bordeaux Cedex</addressLine>
              </address>
            </place>
          </places>
          <functions>
            <function>
              <descriptiveNote>
                <p>Quatre grands domaines de compétence...</p>
              </descriptiveNote>
            </function>
            <function>
              <term vocabularySource="http://data.culture.fr/thesaurus/page/ark:/67717/T1-200">action sociale</term>
              <descriptiveNote>
                <p>1. Solidarité
    blablabla.</p>
              </descriptiveNote>
            </function>
          </functions>
          <legalStatuses>
            <legalStatus>
              <term>Collectivité territoriale</term>
              <citation xlink:type="simple">legal foo</citation>
              <descriptiveNote>
                <p>Description du statut</p>
              </descriptiveNote>
            </legalStatus>
          </legalStatuses>
          <occupations>
            <occupation>
              <term vocabularySource="http://example.org/meeting">Réunioniste</term>
              <dateRange>
                <fromDate standardDate="1987-01-01">1987-01-01</fromDate>
                <toDate standardDate="2099-01-01">2099-01-01</toDate>
              </dateRange>
              <descriptiveNote>
                <p>Organisation des réunions ...</p>
              </descriptiveNote>
            </occupation>
          </occupations>
          <mandates>
            <mandate>
              <term>1. Constitutions françaises</term>
              <descriptiveNote>
                <p>Description du mandat</p>
              </descriptiveNote>
            </mandate>
          </mandates>
          <structureOrGenealogy>
            <p>Pour accomplir ses missions ...</p>
          </structureOrGenealogy>
          <generalContext>
            <p>sous une pluie battante</p>
            <citation xlink:href="http://meteoplouf.net" xlink:type="simple"/>
          </generalContext>
          <biogHist><p>La loi du 22 décembre 1789, en divisant ...</p>
    <p>L'inspecteur Canardo</p><citation xlink:href="http://pifgadget" xlink:type="simple">Voir aussi pifgadget</citation><citation xlink:href="http://www.assemblee-nationale.fr/histoire/images-decentralisation/decentralisation/loi-du-22-decembre-1789-.pdf" xlink:type="simple"/></biogHist>
        </description>
        <relations>
          <cpfRelation cpfRelationType="hierarchical-parent" xlink:href="CG33-DIRADSJ" xlink:type="simple">
            <relationEntry>Gironde. Conseil général. Direction de l'administration et de la sécurité juridique</relationEntry>
            <dateRange>
              <fromDate standardDate="2008-01-01">2008-01-01</fromDate>
              <toDate standardDate="2099-01-01">2099-01-01</toDate>
            </dateRange>
            <descriptiveNote>
              <p>Coucou</p>
            </descriptiveNote>
          </cpfRelation>
          <cpfRelation cpfRelationType="temporal-earlier" xlink:href="whatever" xlink:type="simple">
            <relationEntry>CG32</relationEntry>
          </cpfRelation>
          <cpfRelation cpfRelationType="temporal-later" xlink:href="/dev/null" xlink:type="simple">
            <relationEntry>Trash</relationEntry>
          </cpfRelation>
          <cpfRelation cpfRelationType="associative" xlink:href="http://www.example.org/agent_x" xlink:type="simple"/>
          <resourceRelation resourceRelationType="creatorOf" xlink:href="http://gael.gironde.fr/ead.html?id=FRAD033_IR_N" xlink:role="Fonds d'archives" xlink:type="simple">
            <dateRange>
              <fromDate standardDate="1673-01-01">1673-01-01</fromDate>
              <toDate standardDate="1963-01-01">1963-01-01</toDate>
            </dateRange>
          </resourceRelation>
        </relations>
      </cpfDescription>
    </eac-cpf>
    >>> self.assertXmlValid(generated_eac, self.datapath('cpf.xsd'))
