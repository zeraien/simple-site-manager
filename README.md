# simple-site-manager

This creates configuration files for lighttpd and django fcgi, based on a simple list of sites. 
Templates are used for the output files so they can easily be modified and customised for your own sites.

## Example site list
```yaml
site1:
  domain_name: example.com
  django_root_path: /opt/django/site1/
  max_procs: 3
```

# TODO

- More fine tuning of site performance settings.
