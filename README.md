Description
===========

#### Production

This stack is intended for low to medium traffic production
websites and can be scaled as needed to accommodate future
growth.  This stack includes a Cloud Load Balancer, Cloud
Database, and a Master server (plus optional secondary
servers).  It also includes Cloud Monitoring and Cloud
Backups.

This stack is running the latest version of
[WordPress](http://wordpress.org/about/),
[nginx](https://www.nginx.com/),
and [PHP FPM](http://php-fpm.org/).
with a Cloud Database running
[MySQL 5.6](http://www.mysql.com/about/).


Instructions
===========

#### Getting Started
If you're new to WordPress, the [First Steps With
WordPress](http://codex.wordpress.org/First_Steps_With_WordPress)
documentation will step you through the process of logging into the admin
panel, customizing your blog, and changing your theme.

After the stack has been created, you can find the admin username and
password listed in the "Credentials" section of Stack Details.

The [WordPress Lessons](http://codex.wordpress.org/WordPress_Lessons) cover a
wide range of topics for users and designers.

#### Accessing Your Deployment
If you provided a domain name that is associated with your Rackspace Cloud
account and chose to create DNS records, you should be able to navigate to
the provided domain name in your browser. If DNS has not been configured yet,
please refer to this
[documentation](http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file)
on how to setup your hosts file to allow your browser to access your
deployment via domain name. Please note: some applications like WordPress,
Drupal, and Magento may not work properly unless accessed via domain name.
DNS should point to the IP address of the Load Balancer.

#### Migrating an Existing Site
If you'd like to move your existing site to this deployment, there are
plugins available such as
[duplicator](http://wordpress.org/plugins/duplicator/) or [WP Migrate
DB](http://wordpress.org/plugins/wp-migrate-db/) that can help ease the
migration process.  This will give you a copy of the database that you can
import into this deployment.  There are a number of other tools to help with
this process.  Static content that is stored on the filesystem will need to
be moved manually.  These files should be copied to the Master server, which
will automatically synchronize the contents to all secondary servers.

#### Plugins
There are over 23,000 plugins that have been created by an engaged developer
community. The [plugin directory](http://wordpress.org/extend/plugins/)
provides an easy way to discover popular plugins that other users have found
to be helpful. [Managing
Plugins](https://codex.wordpress.org/Managing_Plugins) is important and you
should be aware that some plugins decrease your site's performance so use
them sparingly.  Please note that some plugins may require you to adjust the
settings for PHP in order for them to function properly.  Please contact
your Support team if you need assistance making these changes.

#### Scaling out
This deployment is configured to be able to scale out easily.  However,
if you are expecting higher levels of traffic, please look into one of our
larger-scale stacks.

#### Details of Your Setup
This deployment was stood up using [Ansible](http://www.ansible.com/).
Once the stack has been deployed, Ansible will not run again unless you update the
stack. **Any changes made to the configuration may be overwritten when the stack
is updated.**

WordPress itself was installed using [WP-CLI](http://wp-cli.org/). WordPress
is installed in /var/www/vhosts/YOUR DOMAIN/ and served by [nginx](https://www.nginx.com/).
The nginx configuration file will be named using the domain name used as a
part of this deployment (for example, domain.com.conf).

Because this stack is intended for lower-traffic deployments, there is no
caching configured.

[Lsyncd](https://github.com/axkibe/lsyncd) has been installed in order to
sync static content from the Master server to all secondary servers.
When uploading content, it only needs to be uploaded to the Master node,
and will be automatically synchronized to all secondary nodes.

MySQL is being hosted on a Cloud Database instance, running MySQL 5.6.
Backups are configured using Cloud Backups.  The Master server is configured
to back up /var/www once per week, and to retain
these backups for 30 days.

Monitoring is configured to verify that nginx is running on both the Master
and all secondary servers, as well as that the Cloud Load Balancer is
functioning.  Additionally, the default CPU, RAM, and Filesystem checks
are in place on all servers.

#### Logging in via SSH
The private key provided with this deployment can be used to log in as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).
This key can be used to log into all servers on this deployment.
Additionally, passwordless authentication is configured from the Master
server to all secondary servers.

#### Additional Notes
You can add additional servers to this deployment by updating the
"server_count" parameter for this stack. This deployment is
intended for low to medium traffic production websites and can be
scaled as needed to accommodate future growth.

When scaling this deployment by adjusting the "server_count" parameter,
make sure that you DO NOT change the "database_flavor" and "database_disk"
parameters, as this will result in the loss of all data within the
database.

This stack will not ensure that WordPress or the servers themselves are
up-to-date.  You are responsible for ensuring that all software is
updated.


Requirements
============
* A Heat provider that supports the following:
  * OS::Heat::RandomString
  * OS::Heat::ResourceGroup
  * OS::Heat::SoftwareConfig
  * OS::Heat::SoftwareDeployment
  * OS::Nova::KeyPair
  * OS::Nova::Server
  * OS::Trove::Instance
  * Rackspace::Cloud::BackupConfig
  * Rackspace::Cloud::LoadBalancer
  * Rackspace::CloudMonitoring::Check
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `wordpress_url`: Domain to use with WordPress Site (Default: example.com)
* `wordpress_sitename`: Title to use for WordPress Site (Default: Example Site)
* `wordpress_user`: Username for WordPress login (Default: admin)
* `wordpress_email`: E-mail Address for WordPress Admin User (Default: admin@example.com)
* `flavor`: Flavor of Cloud Server to use for WordPress (Default: 4 GB General Purpose v1)
* `database_disk`: Size of the Cloud Database volume in GB (Default: 5)
* `database_flavor`: Flavor for the Cloud Database (Default: 1GB Instance)
* `server_image`: Image to use for WordPress (Default: f4bbbce2-50b0-4b07-bf09-96c175a45f4b)
* `server_count`: Number of secondary web nodes (Default: 0)
* `secondary_template`: Template to use for secondary servers (Default: http://catalog.rs-heat.com/wordpress-small/wordpress-small-secondary.yaml)
* `ansible_source`: The Ansible Roles will be pulled from the location provided (Default: http://catalog.rs-heat.com/ansible-roles/ansible-roles.tar.gz)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `wordpress_login_user`: WordPress Admin User
* `wordpress_login_password`: WordPress Admin Password
* `wordpress_public_ip`: Load Balancer IP
* `wordpress_admin_url`: WordPress Admin URL
* `wordpress_public_url`: WordPress Public URL
* `phpmyadmin_url`: PHPMyAdmin URL
* `mysql_user`: Database User
* `mysql_password`: Database Password
* `ssh_private_key`: SSH Private Key
* `server_ip`: Server Public IP
* `secondary_ips`: Secondary Node IPs

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
