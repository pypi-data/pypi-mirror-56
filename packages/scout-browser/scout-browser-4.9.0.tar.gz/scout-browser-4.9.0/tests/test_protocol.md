# Scout validation checklist

## Header:
**Document:** 1369:10 Checklist for functionality testing of Scout

**Category:** Clinical Genomics - Validation

**Issuer:** Emilia Ottosson Laakso

**Approver:** Valtteri Wirta

**Valid date:** 2018-06-14

## Test user and data
All tests are done with the stella.gibson@clinicalgenomics.se unless otherwise stated.
Password: `s#Cr792nw=8SM!cG`

Stella only has access to cust000 and cust003.

Following cases are selected as test cases:
- WGS: epicasp
- WES: cuddlyoryx

## Update staging environment

on rasta (for the CLI):
```
[hiseq.clinical@rastapopoulos ~]$ cd servers/resources/
[hiseq.clinical@rastapopoulos resources]$ update-scout-cli-stage.sh
```

on clinical-db (for the web interface):
```
[hiseq.clinical@hippocampus ~]$ cd servers/resources/
[hiseq.clinical@hippocampus resources]$ bash update-scout-stage.sh
```

## Activate correct environment

For CLI action, please activate the stage environment:
```bash
[hiseq.clinical@rastapopoulos ~]$ cd servers/resources/
[hiseq.clinical@rastapopoulos resources]$ . activate-stage.sh
(stage) [hiseq.clinical@rastapopoulos resources]$ alias scout
alias scout='/mnt/hds/proj/bioinfo/SERVER/miniconda//envs/stage/bin/scout --config /home/hiseq.clinical/servers/config/scout-stage.yaml'
```

## Index page
- [x] Sign in works.
- [x] Version number of Scout shown and correct.
- [x] View case you don't have acccess to and see that you are refused.
- [x] Access a restricted view (https://scout-stage.scilifelab.se/cust000) when logged out. You should not be able to access the restricted view.
- [ ] Access a restricted view (https://scout-stage.scilifelab.se/cust000) when logged out. **Check you are redirected to the restricted view after logging in.**

## Command line
- [ ] Update hpo terms: command `scout update hpo`. Exit code should be zero.
- [ ] Update omim-auto from the cli: `scout update omim`. Check that a new version (current date) was added in the panel view on scout-stage.
- [ ] Update genes: `scout update genes`. Go to genes view and search for `ADK`: should be present and should have transcripts.
- [ ] MT variants:
  - Delete case `~usablemarten~` from scout-stage and load it again (note: used `hotskink`, with 24 MT variants)
  - Count the number of MT variants from the VCF file of this case. To count the number of variants for each chromosome use this script: `grep -v -E '^#' vcf_file | cut -f 1 | sort | uniq -c`
  - Check in scout that all these variants are loaded by filtering the `Clinical SNV and INDELs` by chromosome. Select MT variants only.
  - Check that the special bam file was loaded
  - Check that we can use alignment viewer for MT variants (note: used the beta IGV viewer)
- [ ] Compounds: all compounds for the manually uploaded regions/genes should be visible.
  - Display the list of SNVs for a case: https://scout-stage.scilifelab.se/cust003/18050/variants?variant_type=clinical&gene_panels=IEM
  - Make sure that not all compounds are uploaded for the highest scored variant (Gene MCCC1, coordinates: 3:183015218-183116075 )
  - Upload the variants for the ~MCCC1~ PHKB gene in scout: `scout load region --case-id richfrog --hgnc-id ~6936~ 8927`
  - Check that this time all compounds are uploaded for the variant in the ~MCCC1~ PHKB gene
- [ ] Try to add a new gene panel for cust000 by uploading a CSV file: `scout load panel --help`. A CSV test panel can be downloaded here: http://www.clinicalgenomics.se/scout/static/scout-3-panel-file-example.csv

## Gene Panels page
Overview with gene panels available by institute
- [ ] Gene panels (available from the top-left drop down menu): it should be possible to see old versions of panels (*tests ok*) and *enter those versions*

## Institutes page
First page after logging in.
- [ ] List of institutes correctly shown
- [ ] As "admin" user: all institutes in the database are shown

## Cases
List of cases for any particular institute.
- [ ] Are the WGS and WES cases listed once
- [ ] Assign yourself to a case. A user name is displayed for assigned cases
- [ ] Case status is correct, active for cases where variants have been viewed, prioritized etc.
- [ ] Analysis date is correct
- [ ] Searching:
  - display name
  - sample id
  - assigned user name
- [ ] Searching: hide assigned checkbox hides assigned cases
- [ ] Tags with "wes" and/or "wgs" displayed according to analysis type per sample
- [ ] Check that "rerun" is displayed if case has been uploaded more than once
- [ ] Text under search box reflects number of cases found
- [ ] Prioritized samples show up at the top of the list
  - enter a case and press "Prioritize"
  - go back to list of cases - the case should appear at the top
  - go back to the case and click "De-prioritize", status changes to "active"

## Case page
- Individuals list and pedigree tree (compare with pedigree file)
    - [ ] Sample IDs shown are the customer's sample IDs
    - [ ] Correct family members and relationship
    - [ ] Sex
    - [ ] Affected status (marked with red background in table and according to legend in pedigree tree)
- [ ] "Clinical/research variants" link is functional and takes user directly to the list of variants
- Buttons on left hand sidebar:
  - [ ] Displays "Visualize report" link and report page works. Check that the PDF download works as well
  - [ ] "Archive case": works and colors the sidebar red, "unarchive" returns status
  - [ ] "Request research": confirm message, disables button, new variants uploaded automatically
  - [ ] "Request rerun": confirm message, disables button, opens ticket in Support Systems
  - [ ] "Share case" with cust003: institute list is displayed correctly, sharing now shows "revoke" menu for cust003, revoking works
- [ ] Synposis editor: updating text works
- [ ] Adding diagnosis phenotypes/genes works. Use OMIM:601144.
- [ ] Search and add HPO term `0012335` in the field `Phenotype terms`.

### Comments
- [ ] You can make comments
- [ ] You can remove your own and only your own comments

### Phenotypes
- [ ] You can add phenotype groups and phenotypes (HP:0002795 - Respiratory problems)
- [ ] When you type in a term it autocompletes with related HPO terms
- [ ] Add one HPO phenotype not associated to any gene (test HPO term: HP:0012335)
- [ ] Add "OMIM:601144" and note that "HP:0001699", "HP:0000006", "HP:0001695", "HP:0001663" are added

### Gene panels
- [ ] Should be the same as used for analysis (customer specific - order form)
- [ ] Correct versioning and name
- [ ] Last updated date
- [ ] Number of genes in panel
- [ ] Link on the panel name works
- [ ] External links opens up in new tabs (for example in HPO gene list after Phenotype has been added)
- [ ] Opening research mode adds a button "Research variants" that takes the user to the research list
  - Simulate this by uploading research variants for a case using "scout" command line. `scout load research -i cust000 --case-id FamilyID` (note: used `vitalimpala`)

## Clinical SNVs and indels variants
- [ ] Default gene panels shown (top right)
- Hovering over columns works
  - [ ] 1000 Genomes/PopFreq column - popup shows up
  - [ ] CADD score - popup shows up
  - [ ] Inheritance models - list of compounds
- [ ] "Next page" link works and also to go back by pressing the browser back button
  - [ ] "No more variants to display" is shown when filter doesn't apply to any variants
  - [ ] "Next page" only shows when there are more variants to display
- [ ] Filter - try a set of different filters and combination of the below
  - [ ] Gene panel
  - [ ] Genetic Model
  - [ ] Clinical filter sets up s a preset combination of filters
  - [ ] "Reset filters" under Actions resets all filters (except default panels)
  - [ ] 1000G/ExAC - filters out variants with _higher_ frequency than the number you enter. The format is 0.95 = 95%.
- [ ] Mark as causative should add a link with a badge to the "Case" page and change the status of the case to "solved"
- SNV variant pinning & Sanger:
    - [ ] Pin a SNV variant - should mark variant as interesting (filled in button) and show up in the case view
    - [ ] Place sanger order for pinned variant from the variant view, displays in list in case view (set Sanger email on institute level in mongo db to tester email)
    - [ ] Confirm that the information that is provided in the e-mail is correct and that the e-mail is sent to the correct address
    - [ ] Remove sanger, check that it works as expected
- "Variant tag" dropdown
  - [ ] Select a tag, click save and go back to variant list. Should show up in the variants list (customer specific) by showing a number next to the rank.
- "Dismiss variant" dropdown
  - [ ] Should dismiss the variant (customer specific) by greying out the variant in the variants list
- Frequency
  - [ ] ExAC link opens up in new window and shows correct data. https://scout-stage.scilifelab.se/cust000/P5357-1004fam/e97aa837ad94196632abbf7e16876a1e
  - [ ] 1000G link opens to show more detailed info on the SNP on 1000G webpage. See: https://scout-stage.scilifelab.se/cust000/260566fam30M/fabe068450e6e1d584b3b756779c4138
  - [ ] gnomAD frequency is found when available. Popup and link works.
- Severity. See: https://scout-stage.scilifelab.se/cust000/P5357-1004fam/7adad6a6f2b243005d3927259b218941
  - [ ] Sift is shown when available.
  - [ ] PolyPhen annotation is visible and link opens to form for new submission of query
  - [ ] Check that SPIDEX filter works as expected. Select a SPIDEX level in the filtering view and see that the variants remaining have the corresponding SPIDEX annotation.
- [ ] Expected inheritance models in Gene models shown if annotated in gene list. See: https://scout-stage.scilifelab.se/cust000/P5357-1004fam/7adad6a6f2b243005d3927259b218941
- OMIM phenotypes table. See: https://scout-stage.scilifelab.se/cust000/P5357-1004fam/7adad6a6f2b243005d3927259b218941
  - [ ] Links to correct gene
  - [ ] Shows linked inheritance models
- GT call.
  - [ ] Genotype call and Inheritance model matches. Test this using a variant mapping on the X chromosome. The inheritance model should be XD.
  - [ ] IDs are external customer IDs and matches pedigree tree figure
  - [ ] Support from GATK, Freebayes and samtools is displayed
- Genes, Transcripts and Proteins tables
  - [ ] Links to external webpages opens up in new tab
  - [ ] Transcript shows a "C" badge if canonical and is highlighted in blue if primary in Transcript overview table
- Compounds.
  - [ ] If compound pair link is active it should lead to another variant
  - [ ] Check that columns are filled in for variants with active variant links
  - [ ] The list of compounds is ordered by 'combined score'
- [ ] Summary: Pileup.js alignment viewer and gene coverage present.
- Local observations
  - [ ] shows observations, homozygote, and total number of loaded cases
- Comments
  - [ ] Variant comments work and show up only for cases beloning to the same institute
- Global comments are tagged as such and show up across institutes (note: global comments are tagged as such but are only visble within an institution. Local comments are visible on variant level across the institute)
   - [ ] ~Upload a pre-existing case of cust000 using a different name. Comment globally a variant in the first case and check that the comment is visible in the same variant of newly uploaded case.~
   - [ ] ~Re-upload the first case but under institute cust003. Check that the comment present in the variant of the original case is not visible in the same variant of cust003.~ (note: used variant X_67414426_C_T_clinical to test this in two cust002 and one cust003 case: https://scout-stage.scilifelab.se/cust002/F0015268/5f1a00e07c8e84db619883bbc1f30a9d, https://scout-stage.scilifelab.se/cust002/F0015456/7f870a4f94db24ef34b14bc04edc99e7, https://scout-stage.scilifelab.se/cust003/126/4ce6af6a0d8e0849ffd438a5d86ec560)
- Creating Clinvar submission files
  - [ ] Pin at least one SN variant and one SV for a case and test that the "Submit to clinvar" link works
  - [ ] Fill in the clinvar submission form including case data and test that the file download and save to database options work. Download the submission file and check that each line has a number of fields equal to the fields in the header.
  - [ ] Test that the clinvar submission is visible from the cases and case pages, and that it is possible to delete it from the variant page.

## Clinical SV
Use SV variant
- Pinning works (top right corner)
  - [ ] Pin the variant and check if the SV is shown under "pinned variants" on the case page
- Mark causative works (top right corner)
  - [ ] Mark the variant as causative and check if the SV is shown under "Causative variants" on the case page
- Top left panel
  - [ ] Rank shown
  - [ ] Rank score shown
  - [ ] Category shown
  - [ ] Gene panel shown
 - Top right panel
    - [ ] Position shown
    - [ ] Cytoband shown
    - [ ] Length shown
    - [ ] Type shown
- Frequencies
  - [ ] 1000 Genomes - left and right frequencies are shown
  - [ ] ClinGen CGH - popup shows up
  - [ ] Decipher - popup shows up
  - [ ] Links for Swegen, Beacon and Cosmic are shown (only the first two active) (note: could not test as I couldn't find variants in these databases)
- [ ] Sample genotype nd alleles is displayed (nameless box - below top-right)
  - [ ] ~Caller is displayed in a badge underneat the table~ (note: this is not implemented and should not be tested)
- Genes panel
  - [ ] displays links
  - [ ] check that links are opening in a new tab
- [ ] Check that there exist Overlapping SNVs for this variant:  https://scout-stage.scilifelab.se/cust000/WNB129N/sv/variants/69a5a3dffeda282e3fb1bdeb22d9c34f
- [ ] Bottom of page: three (Ensembl, UCSC, and DECIPHER) outgoing links work

## Alignment page
- [ ] All BAM files for a case are visualized. One per family member.
- [ ] Correct position (+/- 100 bases) is the default window
- [ ] Coverage for each alignment is included
- [ ] Scrolling is possible and loads more parts of the alignment
- [ ] Zoom controls work as expected
- [ ] Jumping to a different chromosome works

## Coverage report (html)
- [ ] Correct samples and display names are shown for the related case
- [ ] For each transcript/sample, overview of mean coverage and all completeness levels shown (note: 15X is not shown in newly analyzed cases due to a bug in mip where the 15X cut-off is not defined in the config file. Issue has been reported: https://github.com/Clinical-Genomics/MIP/issues/533)
- [ ] ~List of non-complete exons are shown for each transcript and sample with links to alignment viewer for that region~ (note: not in current production version and not part of the version changes. Might be old functionality. Not to be tested)
- Customize
  - [ ] "Show genes" checkbox displays gene ids with non-complete transcripts
  - [ ] Changing completeness cutoff updates table "Tackning av transkript vid"
  - [ ] Excluding/changing gene ids updates last two tables

## Coverage report (PDF)
Accessible on the case view.
- [ ] All samples in the case are included with customer ids
- [ ] All text is displayed in Swedish
- [ ] At the top of the report, the name of the panels that the report is based on are displayed (once)
- [ ] Coverage and completeness (all levels) are displayed. (note: not 15X, see comment above)
- [ ] For cust000 the pre-selected completeness level for "transcript coverage" should be 10.
- [ ] The PDF version is equal in terms of content to the HTML version
- [ ] The PDF report for a trio fits on a single A4 page ( https://scout-stage.scilifelab.se/cust000/15035-miptest)

## Gene panel details
Details for a gene panel for a case. Go to a case, click a gene panel.
- [ ] Basic info correct in the "Overview" section
- [ ] Link to "Coverage overview" displayed in the "Overview" section, new tab
  - [ ] Link to "Gene coverage" displayed for each gene in the list

## Coverage overview (within "Overview")
- [ ] Tabs for different levels of completeness are shown and working
- [ ] List of transcripts with completeness shown ranked in order of the metrics
  - [ ] The list updates when different completeness levels are selected
  - [ ] Next/Previous links work if more then 50 transcripts have less than 100% completeness at X coverage
  - [ ] Clicking a gene takes you to specific coverage for that gene and samples"
