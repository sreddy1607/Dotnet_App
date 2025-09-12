4. MotioCI settings and
Cognos instance settings
• Cognos instances and MotioCI
• Cognos Instance Settings tab
• MotioCI settings
• Report Locks tab
• License and security settings
• Configuring cleanup options
• Registering a Cognos instance with
MotioCI
• Editing report output settings
• Unversioned instances
• Unregistering and removing a Cognos
instance from MotioCI
• MotioCI roles
Before you can use the features of MotioCI, you must configure MotioCI
for your Cognos environment.
Administrators generally configure MotioCI early in the business analytics
project life cycle, although you can adjust its settings later.
Motio Proprietary and Confidential
56 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Cognos instances and MotioCI
You can use MotioCI™ with all Cognos® instances that you manage. After you register an instance in MotioCI, you can use its version
control, tracking, testing, and deployment features to work with business analytics content.
MotioCI is designed to complement the “develop-test-release” workflow that most business analytics service teams use in the
development and maintenance of business analytics objects. This workflow uses a separate environment for each phase in the
development process.
Table 9: Typical minimal Cognos deployment
Instance Use Typical users
Development Developing business analytics objects in the Cognos toolset, such
as queries, reports, and analysis objects
Business analytics content
authors on the business
analytics team
Quality Assurance Testing and validating business analytics objects created in the
development instance before they are released to end users
Business analytics content
testers in a QA department
Production End users access and run business analytics objects developed and
tested in the previous two instances
End users in the organization
Integrate MotioCI with all three Cognos instances for version control, tracking, regression testing, and object deployment.
(Other deployment scenarios are possible.) These features simplify your development process for business analytics objects
and help your business analytics team to work more efficiently.
Figure 16: You can integrate a single MotioCI server with multiple Cognos instances
Restricting object output in Cognos instances
In MotioCI you can restrict access to the output generated when regression tests run on business analytics objects in a Cognos
instance.
During regression testing, MotioCI generates outputs (such as XML, CSV, or Excel files) for the business analytics object being
tested. You can configure assertions to analyze the accuracy of this generated output and to ensure that when a business
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 57
analytics object runs, it produces the expected output. MotioCI can retain historical versions of these outputs so that you can
compare different versions of a business analytics object.
You may sometimes wish to restrict access to the outputs of test cases run against certain Cognos instances, such as when
running test cases for sensitive personnel reports against the Production instance. To restrict access, you can “lock down” a
Cognos instance so that only users who have the MotioCI Access Restricted Instance role can access test case output in MotioCI.
By default, every registered Cognos instance in MotioCI is locked down. Because this setting affects all business analytics
objects in the instance, it may have unintended consequences for business analytics service team members who develop and
test objects such as reports in some situations:
• You are asked to create a regression test that tests a report and generates output in HTML and Microsoft® Excel® formats.
• The Development instance is connected to a static baseline of content for testing, but the QA environment is connected to
dynamic, real-world data.
• The QA instance in your organization is locked down, but the Development instance is not.
For more information on restricting access to output, see Restricting access to generated output in an instance.
Motio Proprietary and Confidential
58 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Cognos Instance Settings tab
You can access settings relating exclusively to a selected Cognos instance on the Cognos Instance Settings tab.
When you select a Cognos instance from the Cognos instance tree, the Timeline tab and relevant tabs for the instance appear
in the tab bar in the work area. Click the Cognos Instance Settings tab to configure the selected instance.
Figure 17: Cognos Instance Settings tab, first three field groups: (1) Display, (2) Cognos server, (3) Promotion Sources
Figure 18: Cognos Instance Settings tab, next three field groups: (4) Testing, (5) Security, (6) Schedule
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 59
Figure 19: Cognos Instance Settings tab, last four field groups: (7) Active Versioning Plug-in, (8) Cognos Extensions, (9)
Cognos audit configuration, (10) Other
Display field group
Editing instance name and description
From the Cognos Instance Settings tab, you can edit the name and description of an instance.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
3. In the Display field group, edit the instance Name or Description by typing directly into the text fields.
Configuring the display order of the Cognos instance
On the Cognos Instance Settings tab, you can configure the order in which multiple instances are listed in the Cognos instance tree.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
3. Locate the Display field group.
4. If multiple Cognos instances are registered with this installation of MotioCI, in the Display Order field type the numerical
order in which to display the instance in the Cognos instance tree.
Motio Proprietary and Confidential
60 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Cognos server field group
Cognos reference information fields
Some fields in the Cognos server field group on the Cognos Instance Settings tab are read-only and display information for
reference only.
• Version
• Dispatcher URI
• Gateway URI
• Default Credentials
Editing connection information
On the Cognos Instance Settings tab, you can revise Cognos connection settings.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
3. Locate the Cognos server field group.
4. Click Edit Connection Info.
The Edit Connection Info window opens.
5. In the Dispatcher URI field, edit the URL as needed.
6. Click Test the Dispatcher to verify the connection.
If the dispatcher URL is valid, MotioCI opens a small window showing a section of the Cognos login window.
7. In the Version field, reselect the version if needed.
8. In the Gateway URI field, edit the URI as needed, and then click Test the Gateway.
If the gateway URL is valid, MotioCI opens a small window showing a section of the Cognos login window.
Editing credentials
On the Cognos Instance Settings tab, you can revise credentials for the instance.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 61
3. At the bottom of the Cognos server field group, click Edit Credentials.
The Edit System Credentials window opens.
The number of system credentials can vary. If your instance has exactly one namespace, only one credential is available.
4. Click the Edit icon ( ) for the credential that you want to edit.
5. If Password and API Key are shown, click one to select the credential type.
6. Edit any fields as needed.
• Namespace
• Username
• Password
• API Key (requires Cognos 11.2.4)
7. Click OK.
The updated credential appears in the list in the Edit System Credentials window.
Motio Proprietary and Confidential
62 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
8. You can designate a different namespace as the primary credential by clicking the star icon in the Primary column.
9. To add a credential, click Add and complete the Add System Credentials window.
10. To remove a credential, click its Delete icon ( ).
What is a primary credential?
When creating an instance, you set the primary credential. If you have more than one instance, you can set additional credentials for
them.
Primary credentials are used to version all the public content in an instance. When logged in with primary credentials, you can
version everything within that namespace.
Most users of MotioCI use instances that have only one namespace. However, if you have multiple namespaces, you will need
to log in with additional credentials in order to version users and groups within them.
By using additional credentials, you can version security objects like users and groups and all their content, like My Folders
/ My Content.
About renewing a MotioCI instance session
In the Default Credentials area of the Cognos server field group of the Cognos Instance Settings tab, you can renew the selected
MotioCI instance and end all running worker processes.
When might I need to renew an instance session?
If you update the roles or capabilities for the default credentials user in IBM Cognos Administration, MotioCI does not ordinarily
reflect those changes until you restart the MotioCI service. However, if you need to apply such changes while MotioCI is
running, you can renew the instance session in this section.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 63
What if test cases are currently running?
By default, when you renew an instance session, MotioCI restarts all worker processes. If you restart worker processes while
a batch of test cases is running, test case results may be inconsistent. You can avoid this problem by manually restarting the
worker processes later.
Promotion Sources field group
Restricting promotion sources
With the Promotion Sources setting on the Cognos Instance Settings tab, you can restrict which instances may promote to the
instance.
About this task
By default, promotion from any instance is allowed. Follow these steps if you want to allow promotion only from instances you
specify.
Note: This setting allows or disallows promotion from instances, regardless of user. A related concept is controlling
which instances a particular user may deploy to, as described in Roles and deployment rights.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the instance that will be deployed to; then click the Cognos Instance Settings tab to
open it.
3. In the Policy field of the Promotion Sources field group, clear the Allow from any instance check box.
The Edit button is now enabled. The Sources field displays None or, if promotion was previously restricted, the names of
previously allowed instances.
4. Click Edit.
The Edit Promotion Sources window opens.
5. Select the check box next to each instance that you want to allow promotion from.
6. Click Save to save your changes.
The window closes, and the Sources field now displays the allowed instance or instances.
Motio Proprietary and Confidential
64 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Testing field group
Enabling testing for a Cognos instance
If you have at least one unused testing license, you can enable testing for a Cognos instance in the Testing field group of the Cognos
Instance Settings tab.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you wish to enable for testing and, in the work area on the
right, click the Cognos Instance Settings tab to open it.
3. In the Licensing field of the Testing field group, select the Enable testing for this instance check box.
Any user with the required permissions can now create test cases, test scripts, and assertions for projects on this instance.
In addition, the following user interfaces become available:
• Project Status tab, in the work area on the right
• Assertion Studio node, in the Cognos instance tree
Disabling testing for a Cognos instance
You can disable testing for a Cognos instance in the Testing field group of the Cognos Instance Settings tab, but do so carefully.
Disabling testing will remove any testing-related content created while the feature was enabled.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you wish to disable for testing and, in the work area on
the right, click the Cognos Instance Settings tab to open it.
3. In the Licensing field of the Testing field group, clear the Enable testing for this instance check box.
The Testing Configuration dialog box opens, listing the testing content that will be permanently removed if you continue.
Caution: If you disable testing on an instance on which test cases have already run, those test cases and their
results will be permanently removed, with no way to restore them.
4. Click OK.
MotioCI removes the listed testing content and disables the testing feature for the selected instance, and you will notice
the following changes the next time you log in:
• The instance will no longer display the Project Status tab.
• When updating inheritors on assertions, you will be able to select only instances for which the testing feature is
enabled.
• No users will be able to create test cases, test scripts, or assertions for projects on this instance.
Setting maximum concurrent executions
On the Cognos Instance Settings tab, you can limit the maximum number of executions that MotioCI can run simultaneously.
Before you begin
Access the Cognos Instance Settings tab, as described in Cognos Instance Settings tab. The tab should be open.
About this task
You may wish to lower the number of maximum concurrent executions if your system is having performance issues when
running test cases. A lower maximum may enable your system to run test cases faster.
Procedure
1. In the Max Concurrent Executions field of the Testing field group, revise the default value.
2. Click out of the field to save your change.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 65
Security field group
About the Use Stored Credentials Role Name field
The MotioCI Use Stored Credentials role is a key setting when preparing to configure deployment rights based on user roles.
The Used Stored Credentials Role Name field resides in the Security field group on the Cognos Instance Settings tab. In this
field, you can add or edit the name of the role that determines if a user has permission to use the stored credentials role.
Related information
The system account and its stored credentials
Specifying role-based deployment rights
Restricting access to generated output in an instance
You can restrict access to test output, to protect confidential information. MotioCI uses a special user role for this purpose.
Before you begin
Access the Cognos Instance Settings tab, as described in the Cognos Instance Settings tab topic. The tab should be open.
Procedure
1. Scroll to the Security field group.
2. In the Output and Report Studio Access field, select the "MotioCI Access Restricted Instance" role only check box.
Note: Motio, Inc. recommends locking down only the Cognos environments that contain sensitive production
data.
Related information
Restricting object output in Cognos instances
Schedule field group
Suspending scheduled tasks
On the Cognos Instance Settings tab, you can suspend all scheduled tasks for the Cognos instance.
Before you begin
Access the Cognos Instance Settings tab, as described in the Cognos Instance Settings tab topic. The tab should be open.
Procedure
1. Scroll to the Schedule field group.
2. In the Scheduled Activity field, select the Suspend for this Cognos instance check box.
Note: Selecting this setting does not disable the entire Cognos instance, but only scheduled activity. With this
option selected, you can still run test scripts and test cases manually.
Configuring the versioning schedule for an instance
You can configure the versioning schedule for an instance in the Versioning Schedule window, accessible through the Schedule
field group of the Cognos Instance Settings tab.
About this task
You can set versioning to run on one or more specific days of the week or to run daily. You can also choose the time of day at
which it runs. Alternatively, you can set versioning to run at an interval of a certain number of minutes.
Note: All times displayed in MotioCI reflect MotioCI server time and not client time.
Motio Proprietary and Confidential
66 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
If the active versioning plug-in is installed on your MotioCI application, MotioCI automatically records most of your revisions
when they occur. As a precaution, a scheduled versioning loop runs, picking up changes that MotioCI did not actively version.
Tip: Avoid scheduling two or more instances to version at the same time. Motio recommends setting versioning to
once per day (the default).
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
3. Scroll to the Schedule field group.
4. In the Versioning Schedule field, click Edit.
The Versioning Schedule window opens.
5. From the Type drop-down list, select one of the following schedule types:
• Interval: Enter the time interval (in minutes) in the Interval in Minutes field.
• Daily: Using the check boxes in the Times field, specify times for versioning to run every day.
• Specific Days: Using the check boxes in the Days and Times fields, specify certain days and times to run versioning.
Figure 20: Options to configure the versioning schedule for an instance
6. Click OK.
Note: All times displayed in MotioCI reflect MotioCI server time and not client time.
MotioCI plug-in and extensions
MotioCI includes an optional plug-in and extensions that enable specific features regarding integration with Cognos. Depending on
whether you are using IBM Cognos Business Intelligence (Cognos 10.x) or a release of IBM Cognos Analytics that supports extensions,
you need to download and install different files to use the features that they support.
Cognos Analytics supports use of "extensions" for adding third-party functionality to the interface. To enable you to use this
feature with MotioCI, Motio has developed two plug-ins as Cognos extensions. (For technical reasons, the active versioning
plug-in must remain a plug-in.)
Starting with Cognos Analytics 11.0.5, only the two extensions (authoring integration and Cognos integration) and the active
versioning plug-in are supported. Consult the chart below for a matrix of supported versions.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 67
Starting with MotioCI 3.2.12, the only available plug-in is active versioning. Therefore, because Cognos 10.x does not support
extensions, you can no longer use Cognos integration or Studio integration with it.
Important: In MotioCI 3.5.4, the security of the active versioning endpoint was improved. This change is not
compatible with older versions of the active versioning plug-in. If you upgrade to MotioCI 3.5.4 or later, you must
install the new version of the plug-in.
Table 10: Support matrix for Cognos plug-ins and extensions
Plug-in or extension type Plug-in or extension Cognos releases
10.x 11.0.5 - 12.0.0
Cognos integration plug-in
extension x
plug-in1 Active versioning x x
N/A
Studio (Authoring) integration plug-in
extension x
These extensions and plug-in are specific to each Cognos instance. If you want to install extensions on more than one instance,
for example, on Dev, QA, and Production, publish the extensions from within each Cognos instance. When installing the
plug-in on multiple instances, you can download a single plug-in installer and copy it to each instance.
Note: To install the plug-in on multiple MotioCI Air instances, the plug-in installer must be downloaded from each
instance.
For IBM Cognos Business Intelligence (Cognos 10.x)
Active versioning plug-in for IBM Cognos BI (Cognos 10.x)
For IBM Cognos Analytics (starting with Cognos 11.0.5)
Active Versioning plug-in in IBM Cognos Analytics
Authoring integration extension
Cognos integration extension (Cognos 11.0.5 - 11.1.7)
Cognos integration extension (Cognos 11.2.0 and later)
Related information
Cognos Analytics (Cognos 11) extensions and plug-in
Active versioning plug-in for IBM Cognos BI (Cognos 10.x)
Active versioning plug-in for IBM Cognos BI (Cognos 10.x)
MotioCI uses active and passive version control to identify and record changes to a business analytics object and create its revision
history. Active versioning requires a plug-in.
Passive versioning is installed when you install MotioCI. In passive versioning, the MotioCI server alone checks the Cognos
environment at regular intervals to monitor and capture changes to business analytics objects. This method captures the same
object changes as active version control without requiring you to install the MotioCI plug-in on your Cognos server, but not
immediately. If active versioning is not installed, then your installation of MotioCI can use only passive versioning.
Important: MotioCI plug-ins must be installed on all Content Manager and dispatcher nodes.
Active versioning communicates changes to objects to MotioCI immediately when they occur. Active versioning captures
object changes more quickly than passive version control. If you are using IBM Cognos Analytics (Cognos 11), this plug-in is a
prerequisite for using the Cognos 11 authoring integration extension.
Note: If you need the MotioCI versioning data to include the user name of the person changing an object, you must
use active versioning. Passive versioning cannot record the user name.
1
The plug-in requires JRE 1.8 or later.
Motio Proprietary and Confidential
68 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Downloading the plug-in for a Cognos 10.x instance
The first step in installing the MotioCI active versioning plug-in for use with Cognos 10.x is to download one per instance.
Before you begin
Preconfigure and install MotioCI.
Procedure
1. Log in to MotioCI.
2. From the Cognos instance tree, select the Cognos instance that you wish to configure.
3. In the work area on the right, click the Cognos Instance Settings tab to open it.
4. Scroll to the Active Versioning Plug-in field group.
5. In the Active Versioning field, click Download Installer.
A Zip archive containing the plug-in is downloaded.
Next steps
Installing the plug-in on your Cognos server
Installing the plug-in on your Cognos server
Before you begin
• Preconfigure and install MotioCI.
• Complete the steps in Downloading the plug-in for a Cognos 10.x instance.
About this task
Important: MotioCI plug-ins must be installed on all Content Manager and dispatcher nodes.
Procedure
1. Copy the installation archive to the Cognos installation root directory and extract the archive.
2. Stop the Cognos service.
3. If running MotioCI on a UNIX or Linux system, remember to give the script execute permissions.
4. Run the script below, based on the operating system that your MotioCI application is installed on.
Plug-in Plug-in script Function
installActiveVersioning.cmd
(Win)
Active versioning
./installActiveVersioning.sh (Unix)
Installs the active versioning plug-in.
Note: If installing the plug-in without the MotioCI agent, in MotioCI you must also disable the agent in the
Advanced Configuration tab of the Cognos instance. In the Advanced Configuration tab of the MotioCI root
node, add the host name and port number of the content manager to the Additional CORS allowed
origins property.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 69
5. If the Cognos Application Firewall is running, you may need to add the server that hosts MotioCI to the list of valid domains
and hosts, as follows:
a) Open IBM Cognos Configuration and navigate to Security > IBM Cognos Application Firewall > Valid Domains or
Hosts.
b) Add the server.
c) Save.
6. Restart the Cognos service.
7. In any browser that was pointing to the MotioCI server, refresh the cache or exit and restart the browser.
8. In MotioCI, on the Cognos Instance Settings tab, enable active versioning by selecting the Enable for this Cognos
Instance check box.
Next steps
You can install the plug-in on another server by copying the same installation archive to that server and repeating steps 1 - 9.
Cognos Analytics (Cognos 11) extensions and plug-in
For use with IBM Cognos Analytics, MotioCI includes two optional extensions and one plug-in that enable specific features regarding
MotioCI integration with Cognos.
In IBM Cognos Analytics, you can customize your user interface by using themes and extensions. The new extensions included
with MotioCI use this ability.
These extensions and plug-in are specific to each Cognos instance. If you want to install extensions on more than one instance,
for example, on Dev, QA, and Production, publish the extensions from within each Cognos instance. When installing the
plug-in on multiple instances, you can download a single plug-in installer and copy it to each instance.
Note: To install the plug-in on multiple MotioCI Air instances, the plug-in installer must be downloaded from each
instance.
For Cognos Analytics 11.0.5 and later, MotioCI supports the active versioning plug-in and can publish the other two
(extensions) directly to Cognos.
Downloading the active versioning plug-in (Cognos 11.0.5 and later)
The first step in installing the active versioning plug-in for use with IBM Cognos Analytics is to download a Zip archive per instance.
Before you begin
Preconfigure and install MotioCI.
About this task
Important: In order to use the authoring integration extension, you must first install the active versioning plug-in.
Procedure
1. Log in to MotioCI.
2. From the Cognos instance tree, select the Cognos instance that you wish to configure.
3. In the work area on the right, click the Cognos Instance Settings tab to open it.
4. Scroll to the Active Versioning Plug-in field group.
5. In the Active Versioning field, click Download Installer.
A Zip archive containing the plug-in is downloaded.
Next steps
Install the active versioning plug-in, as described in Installing the plug-in on your Cognos server.
Motio Proprietary and Confidential
70 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Publishing extensions directly to Cognos (Cognos 11.0.5 and later)
If you have a release of IBM Cognos Analytics that supports extensions, you can publish two extensions directly from MotioCI.
Before you begin
Install the active versioning plug-in, as described in Installing the plug-in on your Cognos server.
About this task
The extensions can easily be published to Cognos Analytics. The Active Versioning plug-in must be installed manually.
Procedure
1. In the Cognos instance tree on the left, select the instance of Cognos Analytics that you wish to add extensions to.
2. In the work area on the right, click the Cognos Instance Settings tab to open it.
3. Scroll to the Cognos Extensions field group.
4. In the Authoring Integration Extension field, click Publish.
MotioCI publishes the extension to Cognos and notifies you that the extension was successfully published.
Note: To use authoring integration without the MotioCI agent, in the Advanced Configuration tab of the Cognos
instance set the Enable MotioCI agent property to false, and in the Advanced Configuration tab on the
MotioCI root node add the host name and port number of the content manager to the Additional CORS
allowed origins property.
5. In the Cognos Integration Extension field, click Publish.
MotioCI publishes the extension to Cognos and notifies you that the extension was successfully published.
Active Versioning plug-in in IBM Cognos Analytics
MotioCI uses active and passive version control to identify and record changes to a business analytics object and create its revision
history. Active versioning requires a plug-in.
Passive versioning is installed when you install MotioCI. In passive versioning, the MotioCI server alone checks the Cognos
environment at regular intervals to monitor and capture changes to business analytics objects. This method captures the same
object changes as active version control without requiring you to install the MotioCI plug-in on your Cognos server, but not
immediately. If active versioning is not installed, then your installation of MotioCI can use only passive versioning.
Important: MotioCI plug-ins should be installed on all Content Manager and dispatcher nodes. If your network setup
prevents you from installing the plug-in on all dispatchers, contact Motio Support for a possible workaround.
Active versioning communicates changes to objects to MotioCI immediately when they occur. Active versioning captures
object changes more quickly than passive version control. If you are using IBM Cognos Analytics (Cognos 11), this plug-in is a
prerequisite for using the Cognos 11 authoring integration extension.
Note: If you need the MotioCI versioning data to include the user name of the person changing an object, you must
use active versioning. Passive versioning cannot record the user name.
Authoring integration extension
The authoring integration extension enables you to check out reports from within the Cognos authoring perspective (also known as
Cognos Analytics - Reporting). In addition, it allows you to enable broadcast messaging.
The authoring integration extension is designed for use with IBM Cognos Analytics. This extension adds functionality to
Cognos to allow users to check out reports, preventing other users from saving changes to the report while it is checked out. In
addition, you must install the authoring integration extension if you wish to use broadcast messaging.
Important: In order to use the authoring integration extension, you must first install the active versioning plug-in.
If you have Cognos 11.0.5 or newer, you can publish the extension from within MotioCI directly to Cognos.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 71
Cognos integration extension (Cognos 11.0.5 - 11.1.7)
Cognos integration is a portal to the revision history of an item through the navbar of the welcome portal.
The Cognos integration extension is required if you want to enable users to log in to MotioCI by using Cognos portal
authentication.
To enable Cognos integration, you must publish the MotioCI Cognos integration extension or install the plug-in, as described
in Publishing extensions directly to Cognos (Cognos 11.0.5 and later).
After the extension is published, two MotioCI user interface elements appear in the IBM Cognos Analytics user interface:
• At the bottom of the context menu for an artifact, a View Revision History menu item
• At the bottom of the navbar on the Welcome portal, the MotioCI Cognos ninja icon
Selecting View Revision History opens the Cognos Integration portal, from which you can perform various actions on
revisions, such as rolling back, deploying, and comparing two versions of an object.
At the bottom of the navbar on the Welcome portal, you can click the MotioCI icon to access MotioCI.
Motio Proprietary and Confidential
72 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Cognos integration extension (Cognos 11.2.0 and later)
Cognos 11.2.0 has a new interface, so elements added by the Cognos integration extension have changed location.
You can publish the extension by following the steps in Publishing extensions directly to Cognos (Cognos 11.0.5 and later). After it
is published, MotioCI user interface elements appear in the Cognos Open menu and in the Action menu for artifacts.
Figure 21: In the Open menu, a menu item (with the MotioCI icon) for accessing MotioCI
Figure 22: The View Revision History menu item for an artifact
The Cognos integration features are the same as in previous versions of Cognos Analytics.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 73
Selecting View Revision History opens the Cognos Integration portal, from which you can perform various actions on
revisions, such as rolling back, deploying, and comparing two versions of an object.
In addition, this extension is required if you want to enable logging in to MotioCI with Cognos portal authentication.
CAM Passport Login Fix extension
In Cognos Analytics 11.1.1, a bug was introduced that breaks the user session when a MotioCI user clicks a direct link to Cognos in the
MotioCI interface. This extension fixes the problem caused by that bug.
The bug introduced in 11.1.1 prevents user preferences from loading, causing problems when running reports and when
adding new steps to jobs. If you are using an instance of Cognos Analytics 11.1.1, publish this extension to ensure that you can
access Cognos via a direct link within MotioCI without experiencing these issues.
The link to the extension displays under the other extensions in the Cognos Extensions field group on the Cognos Instance
Settings tab.
Cognos audit configuration field group
Setting up MotioCI to use Cognos auditing
Before using the inventory feature, you must set up MotioCI to use information gathered by Cognos auditing.
Before you begin
• Ensure that your Cognos environment is using the Cognos audit database.
• Gather configuration information about the database from your Cognos administrator.
Procedure
1. In the Cognos instance tree, select the Cognos instance for which to set up the inventory feature.
Several tabs display in the tab bar, including a Warehouse tab and an Inventory tab.
2. In the Cognos audit configuration field group on the Cognos Instance Settings tab, click Add.
The Add Cognos Audit Configuration dialog box opens.
3. Do one of the following:
• If the audit package for this instance is located in the same instance, leave the default value, The same instance
[Instance Name], selected.
• If the audit package for this instance is located in another instance, select A different instance and then select the
instance from the adjacent drop-down box.
4. Click Next.
Four new fields appear in the dialog box:
• Audit Package
• Data Source
• Data Source Connection
• Data Source Signon
Motio Proprietary and Confidential
74 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
5. In Edit drop-down list in the Audit Package field, select one of the following:
• Select Object
• Enter Search Path
6. If you selected Select Object, navigate to the desired audit package in the Select Audit Package window that opens, and
click OK.
The path to the selected audit package appears in the Audit Package field.
7. If you selected Enter Search Path, enter the path to the audit package in the Enter Search Path dialog box that displays,
using the format shown here, and click OK:
/content/package[@name='My Audit Package']
8. Follow the same steps for the Data Source field to select the data source.
The data source connection and data source sign-on values appear in those respective fields.
9. Click Finish.
The Test Audit Configuration window opens. MotioCI performs several tests on the audit configuration and displays their
results in the window. For more about this window, see Editing, testing, or deleting the Cognos audit configuration.
10. Click Close.
MotioCI saves your settings and displays the updated Warehouse tab, showing several sections that are empty or
populated with default values:
• Schedule: Shows a default schedule, along with Edit and Run Now buttons.
• Cognos Audit: Includes Last Run and Status fields. The default value of Status is This job has not yet been
run.
• MotioCI Statistics: Includes Last Run and Status fields. The default value of Status is This job has not yet
been run.
• ETL Cleanup: Includes Last Run and Status fields. The default value of Status is This job has not yet been
run.
• History: Shows an empty table, with the following columns:
• Job
• Started
• Duration
• Status
Editing, testing, or deleting the Cognos audit configuration
After you have set up MotioCI to use Cognos auditing, you can edit the configuration, test it again, or delete it.
Before you begin
Complete the steps in Setting up MotioCI to use Cognos auditing.
Procedure
1. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
2. Scroll to the Cognos audit configuration field group.
3. Optional: Click Edit.
The Edit Cognos Audit Configuration dialog box opens. It is identical to the Add Cognos Audit Configuration dialog box
except that, after you complete it, MotioCI does not automatically perform tests.
4. Optional: Edit the configuration by following the same steps as in Setting up MotioCI to use Cognos auditing.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 75
5. Optional: Click Test.
The Test Audit Configuration window opens. MotioCI performs several tests on the audit configuration. The test results
are displayed in the window, and for each test a colored icon indicates success ( ), warning ( ), or failure ( ). For an
explanation of each test, see About Cognos audit configuration tests.
6. Optional: Click the plus icon ( ) next to each test to view detailed results.
7. Click Close.
8. Optional: To delete the Cognos audit configuration, click Delete and then click Yes.
MotioCI deletes the Cognos audit configuration and all related jobs and job execution history.
Motio Proprietary and Confidential
76 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Other field group
Publishing MotioCI reports to the current Cognos instance
You can publish MotioCI reports to the current instance on the Cognos Instance Settings tab.
About this task
Important: The MotioCI reports package supports only Cognos 11.1.7 and later.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
The MotioCI user interface loads, with the Project Status tab open.
2. In the Cognos instance tree, select the name of the instance that you want to edit and, in the work area on the right, click
the Cognos Instance Settings tab to open it.
3. Scroll down to the Other field group.
4. In the MotioCI Reports field, click Publish.
5. If you are warned of a previously installed version of the reports package, click Yes to update the existing package.
MotioCI publishes the reports to the current Cognos instance and notifies you when done.
MotioCI settings
Normally, administrators configure general settings for MotioCI when accessing MotioCI for the first time after installation. You can,
however, modify your general MotioCI settings: for example, if you upgrade your MotioCI installation or need to change certain
properties, such as mail server settings.
Note: To configure settings for MotioCI, you must have the MotioCI Administrator role. For more information about
upgrading MotioCI, consult the MotioCI Installation and Upgrade Guide.
Related information
Configuring external ticket references
MotioCI roles
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 77
MotioCI Settings tab
You can access configuration tools and settings for MotioCI on the MotioCI Settings tab.
Figure 23: MotioCI Settings tab, first four sections: (1) Version control and deployment, (2) Testing, (3) Browser Service
Configuration, and (4) Email settings
Motio Proprietary and Confidential
78 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Figure 24: MotioCI Settings tab, last four sections: (5) Network settings, (6) Third-party ticketing integration, (7) User
interface, and (8) Advanced settings and monitoring
Accessing MotioCI settings
The MotioCI Settings tab is available in the tab bar when you log in to MotioCI.
Procedure
1. Log in to MotioCI as a user with the MotioCI Administrator role.
2. If you are already logged in and the MotioCI root node is not currently selected, select it now in the Cognos instance tree.
The tab bar loads in the work area, including all associated tabs..
3. Click the MotioCI Settings tab.
Options appear for configuring MotioCI.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 79
Version control and deployment field group
Configuring versioning and deployment settings
You can fine-tune MotioCI versioning and deployment settings in several ways.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
About this task
The Version control and deployment field group is the first section on the tab.
Procedure
1. In the Version Numbers field, select or clear the check boxes next to the following options to enable or disable them for
each version of an object:
• Hide client version number
• Hide MotioCI revision number
Tip: In order to see the effects of these changes, clear the cookies in your web browser.
2. In the Authoring Check-Ins field, accept the default setting (Mark as major by default or clear the check box, which will
change the default revision type to "minor" when a user checks in an object in Cognos.
3. Optional: If you wish to require a user to enter a comment when checking in a revision marked as “major,” in the Major
Revisions field select the Require comments on check-in check box .
4. Optional: If you wish to use pattern-matching for major check-ins to enforce a specific format, type the regular expression
that you wish to use in the Major Revision Regex field.
Thereafter, when a user enters a comment, MotioCI checks it and allows only those comments that match the pattern.
5. Optional: If you want the deployment to disregard any references that are invalid, in the Ignore invalid references field,
select the Ignore during deployment by default check box.
Related information
Worker processes
Report Output Directory field
MotioCI settings
Motio Proprietary and Confidential
80 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Configuring recommended maximum diff size
For performance reasons, you may wish to limit the size of diffed output.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. In the Version control and deployment field group, locate the Recommended Max Diff Size field.
2. Enter a size (in megabytes) to set as the maximum allowed for a diff.
3. Click out of the field to save the new setting.
Testing field group
Disabling Assertion Studio
Assertion Studio, enabled by default, is a tool for authoring custom assertions. If you do not wish to create custom assertions, you can
disable Assertion Studio.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. In the Testing field group, locate the Assertion Studio field.
2. Clear the Enable Assertion Studio check box.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 81
Setting defaults for generating and running tests upon check-in
If you know whether you wish to generate or run tests when an artifact is checked in, you can set the defaults on the MotioCI
Settings tab.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Locate the Testing field group, the second section on the tab.
2. In the Generate Tests upon Check-In field, accept the default setting (Yes by Default) or select from the following
other options:
• Always
• No by Default
• Never
Thereafter, when a user checks in an object, MotioCI applies your choice to determine whether to generate tests.
3. In the Run Tests upon Check-In field, accept the default setting (Yes by Default) or select from the following other
options:
• Always
• No by Default
• Never
Thereafter, when a user checks in an object, MotioCI applies your choice to determine whether to run tests.
Report Output Directory field
This field is read-only.
The Report Output Directory field appears in the Testing field group and displays the currently configured directory for
report output, which is set during MotioCI installation.
Worker processes
MotioCI runs all test cases in a multiprocess format. These processes are called worker processes.
You can configure the number of processes spawned for your MotioCI environment. Each worker has a number of threads
that perform the tasks associated with running a test case (validation, execution, running assertions). Each part of the test
Motio Proprietary and Confidential
82 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
case executes independently. The worker process can thereby execute multiple test cases at the same time. Because MotioCI
processes the different tasks of an execution in this way, long-running test cases do not block other test cases from running.
Figure 25: Worker Processes tab
Table 11: Columns in the Worker Process table
Column Description
ID ID of the worker process.
Created Date and time that the process was created.
Last Updated Date and time that the process was last updated.
Status Current status of the process.
Possible values:
Started: The processes is currently running.
Terminating: The process was killed and is wrapping up current work.
Terminated: The process is dead.
Process ID ID returned by the operating system when the process is created.
Host Name Name of the machine on which MotioCI is installed.
Working Directory Path to the directory on the file system associated with the process.
Why the process terminated.
Possible values:
Exited: The process was killed.
Unlively: Two minutes have lapsed, and the process did not check in with
MotioCI. Each process has a thread designed to check in with MotioCI
periodically. MotioCI marks the process as unlively and replaces it with
a new process.
Shutdown Reason
None: The process is still running.
Actions If the worker processes is still alive, a Kill Process link displays.
Related information
Viewing current worker processes
Viewing all worker processes (past and present)
Ending a worker process
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 83
About worker process settings
By default, the worker process log is a separate file from the main MotioCI log. In this section, you can configure whether or not
MotioCI appends the worker process log to the MotioCI-Main-Process.log.{current date} file.
MotioCI can use worker processes for greater scalability and to give you the option to run more tests. Worker processes use
available RAM on your MotioCI server to accomplish their work. Each time the MotioCI main process creates a new worker
process, it assigns it a unique numerical ID, which is recorded in the MotioCI database.
Tip: This setting increases the load on system resources. Enable this setting temporarily, only for troubleshooting
purposes.
If you are concerned about memory usage, you can limit the number of worker processes that can run simultaneously.
Configure this setting in the Number of Worker Processes field. The default setting is 1.
Tip: As a general rule, consider that each worker process consumes about 1 GB of RAM. Using that assumption, you
can determine a reasonable maximum number or worker processes based on how much free memory your server
ordinarily has.
Configuring worker process settings
You can append worker process logs to the MotioCI application log and set the maximum number of worker processes.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Locate the Testing field group.
2. In the Worker Process Log field, clear or select the Append Worker Process Logs to Application Log check box to set
MotioCI to keep the logs separate or append them.
3. In the Number of Worker Processes field, type the minimum number of worker processes for MotioCI to spawn.
4. Optional: If you wish to view a list of current worker processes, in the Worker Processes field click Manage.
Viewing and ending worker processes
In the Testing field group on the MotioCI Settings tab you can access worker processes to evaluate whether to end any.
Viewing current worker processes
You can view a list of current worker processes.
Procedure
1. In the Cognos instance tree, click the root MotioCI node.
The associated tabs appear in the work area on the right.
2. Click the MotioCI Settings tab to open it.
Motio Proprietary and Confidential
84 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
3. Locate the Testing field group.
4. In the Worker Processes field, click Manage.
The Worker Processes tab opens, displaying all current worker processes.
Viewing all worker processes (past and present)
You can view a list of all processes, past and present.
Before you begin
Follow the instructions for Viewing current worker processes.
Procedure
1. In the Cognos instance tree, click the root MotioCI node.
The associated tabs appear in the work area on the right.
2. Click the MotioCI Settings tab to open it.
3. Locate the Testing field group.
4. In the Worker Processes field, click Manage.
The Worker Processes tab opens, displaying all current worker processes.
5. In the menu bar, select the Show All Processes check box.
The table displays all worker processes, past and present.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 85
Ending a worker process
From the MotioCI Settings tab you can end one or more running worker processes.
Before you begin
• Follow the instructions for Viewing current worker processes.
• You should be on the Worker Processes tab.
Procedure
1. In the Actions column of the worker process that you wish to end, click Kill Process.
2. Click OK in the confirmation window.
The status of the killed process changes to Terminating while the process wraps up work and, upon completion,
displays as Terminated.
Figure 26: Worker processes table showing Kill Process links
Important: When you end a worker process, MotioCI halts all test cases and other processes running on that
worker process.
Configuring browser service
To enable multi-page HTML output for Cognos objects in MotioCI, configure the browser service.
Before you begin
• Download the browser service archive provided to you by your Motio representative, and extract it to any location.
• To install as a Windows service, run installBrowserService.cmd in an admin console.
• Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Scroll down to the Browser Service Configuration field group.
Figure 27: Browser Service settings configured for MotioCI
2. Click Edit.
The Edit Connection Info dialog box appears.
3. In the Host name field, accept the default value, localhost, or enter the IP address or DNS-resolvable name of the
computer on which you will run the browser service.
4. In the Port number field, accept the default value of 30008, or if the browser service will run on a different port, enter a
different port number.
5. Click Save.
6. Click Download Configuration.
7. In the Save As window that appears, navigate to the folder containing the browser service and then click Save.
8. Execute one of the following, depending on your operating system:
Motio Proprietary and Confidential
86 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
Windows:
{extracted-archive-directory}\browser-service.exe
UNIX or Linux:
{extracted-archive-directory}/startBrowserService.sh
The browser service will extract the configuration archive and begin running.
9. Optional: Click Test to open a pop-up window verifying that the browser service is running.
Configuring email settings
You must configure the email settings for your organization before MotioCI can send email notifications to users.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Scroll down to the Email settings field group.
Figure 28: Email settings configured for MotioCI
2. In the SMTP Host field, type the server address (such as mail.example.com) of the mail server that will handle email traffic
from MotioCI.
3. In the SMTP Port field, type the port number that your mail server uses.
4. In the next two fields, select whether for SMTP security you will Use SSL, whether your system will Require user name and
password, or both.
Note: If the mail server for MotioCI does not support anonymous sending of emails, select the Require user
name and password check box and ensure that the email user name and password supplied are valid user
credentials. Otherwise, MotioCI may be unable to send email.
5. In the User Name field, type the user name for the email account set up for MotioCI.
6. In the Password field, type the password for the email account set up for MotioCI.
7. In the From Address field, type the email address that notification messages will appear to originate from.
8. Click Send a Test Email to verify that your email settings are configured correctly.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 87
Network settings field group
Configuring application server settings
The Application Server URL field displays the URL that users point their web browsers to in order to access the MotioCI user
interface. This field is read-only and for informational purposes only.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Scroll down to the Network settings field group.
2. In the Application Server Host field, type the URI of your application server, allowing MotioCI to communicate with
Cognos and your business analytics environment through the MotioCI plug-in/extensions.
Configuring HTTP proxy server settings
MotioCI must access the Internet when a user submits a ticket to the Motio Customer Support site. If the MotioCI server requires a
proxy server to access the Internet, you may want to configure the proxy server information within MotioCI.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Scroll down to the Network settings field group.
2. In the HTTP Proxy Server field, click Edit.
The MotioCI Server HTTP Proxy Configuration dialog box opens.
Motio Proprietary and Confidential
88 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
3. Type the Host Name, Port, User Name, and Password for the proxy server.
4. Click OK.
Note: This feature requires that the proxy server support basic authentication.
Third-party integration settings field group
You can configure MotioCI to integrate with a third-party ticket-tracking application to automatically link ticket references in MotioCI
to the actual tickets in the tracking program.
Note: This topic just lists the fields in the Third-party ticketing integration field group on the MotioCI Settings tab.
For detailed information about integrating MotioCI with third-party ticketing systems, see Using MotioCI with thirdparty ticketing systems.
In the Third-party ticketing integration field group, you can set the ticket link format, the ticket command, and the ticket
identifier format for your ticketing system.
For example, if major check-ins must reference an external ticket number (for example, wo #12345), you could use the
following regular expression:
".*wo[ ]?#.*"
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 89
Configuring pagination settings
In the User interface field group of the MotioCI Settings tab, you can configure the length of dynamic pages in the MotioCI user
interface. When a table or tree reaches the maximum length, MotioCI displays the content in multipage form.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
Procedure
1. Scroll down to the User interface field group.
2. In the Tree Page Size field, accept the default value of 25 or type another value to determine the maximum number of
nodes that MotioCI displays in a tree before paging the content.
3. In the Grid Page Size field, accept the default value of 25 or type another value to determine the maximum number of
grid rows that MotioCI displays on a single screen before paging the content.
Advanced settings and monitoring field group
Downloading MotioCI logs
You can download logs to help with troubleshooting.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
About this task
When downloading MotioCI log files, you have two basic options:
• Download all logs for a range of recent days
• Manually select which logs to download
Procedure
1. Scroll to the Advanced settings and monitoring field group at the bottom of the MotioCI Settings tab.
2. In the MotioCI Logs field, click Download.
The Download MotioCI logs dialog box opens.
3. If you wish to download all logs for a range of recent days, in the Number of days of logs to download (including today)
field, accept the default value or change it to indicate how many days of logs you wish to download.
4. Click OK.
MotioCI downloads a Zip archive containing all of the logs for the number of days that you indicated.
Motio Proprietary and Confidential
90 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
5. If you wish to manually select which logs to download, click Select Individual Logs.
A window opens showing a list of available server logs.
Note: If you previously selected the number of days to download, logs from those days appear in the list
preselected.
6. Select the check box next to any unselected logs that you wish to include, and clear the check box next to any log that you
wish to omit from the archive.
7. Click OK.
MotioCI packages the selected logs in to a single Zip archive, and your web browser prompts you to open or save the
archive of selected log files.
Accessing MotioCI logs when MotioCI is not running
You can obtain a Zip archive of MotioCI logs even if you cannot access the user interface of a running MotioCI server.
Procedure
1. Log on to the computer on which MotioCI is installed.
2. Change to the MotioCI installation directory.
3. Execute one of the following, depending on your operating system:
Windows:
{MotioCI-installation-directory}\createSupportZip.cmd
UNIX or Linux:
{MotioCI-installation-directory}/createSupportZip.sh
Next steps
Attach the generated Zip archive to your MotioCI support case or email.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 91
Monitoring MotioCI application settings
On the MotioCI Application Monitoring tab, you can monitor the CPU usage, memory usage, database connections, and more
data about the MotioCI application server.
Before you begin
Access the MotioCI Settings tab, as described in Accessing MotioCI settings. The tab should be open.
About this task
You must be logged in as a MotioCI administrator in order to access this feature.
Procedure
1. Scroll to the Advanced settings and monitoring field group at the bottom of the MotioCI Settings tab.
2. In the Application Server Monitoring field, click Launch.
The MotioCI Application Monitoring tab opens, displaying real-time data about:
• Process CPU
• System CPU
• Java Heap Memory
• System Physical Memory
• Database Connections
• Database Properties
• Thread information
Note: Depending on the width of your browser window, you may need to scroll to the right to see the MotioCI
Application Monitoring tab.
Advanced MotioCI settings
The Advanced Configuration tab is reserved primarily for properties that you may need to modify for less common tasks, such as
when troubleshooting with the help of MotioCI technical support.
You must have the MotioCI Administrator role to access this tab and to see the Advanced MotioCI Settings hyperlink on
the MotioCI Settings tab or the Project Settings tab or the Advanced Instance Settings hyperlink on the Cognos Instance
Settings tab.
Note: Most of the properties listed on the Advanced Configuration tab are highly technical. Motio®, Inc. expects that
most MotioCI administrators will rarely, if ever, need to adjust these settings. These properties are exposed here as a
convenience for the few who may need to adjust them.
Motio frequently adds new advanced properties. Their names and descriptions are available within the user interface. You can
access advanced settings in a few ways.
• Go to the MotioCI Settings > Advanced settings and monitoring > Configuration Properties field and click the
Advanced MotioCI Settings link (for general MotioCI settings)
• Go to the Cognos Instance Settings > Configuration Properties field and click the Advanced MotioCI Settings link (for
advanced settings specific to a Cognos instance)
• Go to the Project Name > node Project Settings tab > Configuration Properties field and click the Advanced MotioCI
Settings link (for advanced settings specific to a MotioCI project)
Motio Proprietary and Confidential
92 | MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings
You can filter the list by category and can group the list by level, category, or name. To see descriptions for each property, click
the information icon ( ) next to the Filter by category drop-down list.
Figure 29: Snapshot of some of the advanced properties, as of Oct. 23, 2018 (likely to change)
Table 12: Sample Advanced Configuration tab properties available when accessed from the Cognos Instance Settings
tab
Property Description
Assumed Cognos version Versioned items created before MotioCI 3.1 did not record the version of Cognos. Set
the assumed version for these items to one of the following: cognos8_4, cognos
10_1, cognos 10_1_1, cognos 10_2, cognos 10_2_1, cognos 10_2_2.
Deployment authentication types Set a comma-separated list of visible authentication types for deployment. Options are
Standard and Portal
Require successful impact analysis Require all promotions to pass the impact analysis test before promoting
... and more
Table 13: Sample Advanced Configuration tab properties available when accessed from the MotioCI Settings tab
Property Description
Audit Cognos service main Log Cognos activity of the main process to a log file
Cognos portal authentication
timeout
Seconds to wait when using portal authentication to retrieve an existing Cognos session
Enable supported browser check Check if your web browser is supported and display a message if it is not
General authentication types Set a comma-separated list of visible authentication types for logging in to MotioCI.
Options are Standard and Portal
Info level request timeout threshold HTTP timeout threshold (seconds) at which an information-level statement is logged
Kill unfinished worker processes on
startup
Kill unfinished worker processes when MotioCI starts
Mail max attachment size Maximum combined size of all mail attachments, in megabytes
Optimize versioning for new objects Optimizes the versioning of new objects. Set to "true" if objects are frequently added to
Cognos and "false" otherwise.
Motio Proprietary and Confidential
MotioCI Administrator's Guide | 4. MotioCI settings and Cognos instance settings | 93
Property Description
Refresh interval for Project Status
tab
Automatic refresh interval (in seconds) for the Project Status tab
Temp folder path Cognos search path for the MotioCI staging folder
Validation command for external
promotions
The command to use to validate deployments. All deployments must pass this test to be
allowed to run.
... and many more
Resetting one or more advanced settings
On the Advanced Configuration tab you can restore any modified advanced setting to its default. You can reset one setting or reset
several (or all) in bulk.
Before you begin
Caution: Ensure that you know which settings you wish to reset. This feature has no "Undo" function.
Procedure
1. Access the Advanced Configuration tab, as described in Advanced MotioCI settings.
2. Select the check box in the left margin in the main work area for each property that you wish to reset.
3. In the toolbar click Reset.
A dialog box opens showing the settings that will be reset to default values.
4. Click OK to reset to defaults
