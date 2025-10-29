---
title: "Ansible Release 12: the Windows Vista Moment"
date: 2025-11-03 07:44:00+0100
tags: [ Ansible ]
---
My [first encounter](https://github.com/ipspace/netlab/issues/2683) with Ansible release 12 wasn't exactly encouraging. We were using a few Ansible Jinja2 filters (**ipaddr** and **hwaddr**) in internal _netlab_ templates, and all of a sudden those templates started crashing due to some weird behavior of attributes starting with underscore.

We implemented *[don't use Ansible release 12](https://github.com/ipspace/netlab/pull/2684)* as a quick workaround, but postponing painful things is never a good solution(see also: visiting a dentist), so I decided to try to make _netlab_ work with Ansible release 12. [What a mistake to make](https://www.youtube.com/watch?v=n-PEUuzMlWg).
<!--more-->
Here's what I found before I hit a major showstopper:

### When Conditions

The Ansible module/block **when** conditions were evaluated as Python boolean expressions, which means that a non-empty string (for example) would be *True*. Ansible release 12 expects them to produce a *True*/*False* result.

To make matters worse, due to the way Python evaluates boolean expressions, `a and b` results in value of **b**, not in *True*/*False* value, which means that most **when** expressions, even when they include boolean operators like **and** or **or**, might result in non-boolean results (**not** is the only exception).

Rubbing some salt into this open wound: according to Ansible documentation, the **[first_found](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/first_found_lookup.html)** lookup could return the file name, or an empty list or *None* when the file is not found.

I could use the **[truthy](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/truthy_test.html)** test on every **when** expression, but decided to go for a more verbose `x is string and x != ''`.

There is an Ansible environment variable that you can set to revert to the old behavior, but that just prolongs the pain.

### Macro Results

In older Ansible releases, a Jinja2 macro that resulted in no text returned an empty string. With release 12, the same macro returns *None*. I have no idea whose fault that is, but it sucks.

This is how we were using Jinja2 macros with `indent` filters to generate configuration blocks that could be used in various places in the device configuration hierarchy (for example, you could have the **redistribute** command under **router** or **router/address-family** sections):

```
{{ some_config()|indent(2,first=True) }}
```

That no longer works in Ansible release 12. You have to check the results of the macro and use **indent** only if they are *truthy*, for example:

```
{% set redist_cfg = some_config() %}
{% if redist_cfg %}
{{   redist_cfg|indent(2,first=True) }}
{% endif %}
```

Whoever caused this change, thank you for the roses (I guess).

### Tests of Undefined Variables

In the previous Ansible releases, `x is string` would be *False* if **x** was not defined. Now, the same test throws an error; you have to use something along the lines of `x is defined and x is string`.

I'm not blaming anyone for this change (after all, throwing an error is the correct response), but imagine how many hard-to-find errors this will trigger.

### Some Built-In Filters Must Use FQDN Names

For whatever reason, using the **ipaddr** filter throws an error. You have to use **ansible.utils.ipaddr**. OTOH, you can still use **ios_config** instead of **cisco.ios.ios_config** module.

For extra fun, the change (if it was intentional) is not mentioned in the [Ansible 12 Porting Guide](https://docs.ansible.com/ansible/devel/porting_guides/porting_guide_12.html#porting-guide-for-v12-1-0) (or maybe I missed it, I only searched that page for `.utils`).

### The Showstopper: Using Templates in Device Configuration Modules

Since days immemorial, device configuration modules (for example, **ios_config** or **eos_config**) have accepted a Jinja2 template in the **src** parameter and rendered the template before pushing the configuration to the device (that's also what the documentation claims).

It looks like at least **ios_config** and **eos_config** modules (in short- and FQDN form) no longer render the template but try to push Jinja2 code to the device. The device is not amused.

Of course, I could work around that. I could render the template into a local temporary file and push that file to the device, but I decided I would [rather wait](https://github.com/ipspace/netlab/issues/2768) to see if someone gets annoyed enough to have the error fixed.

I also installed the **ansible.netcommon** (8.1.0) and **arista.eos** (12.0.0) collections (the versions packaged with Ansible release 12.0) on top of Ansible release 11.10, and they work (modulo the **ipaddr** quirk). The problem is thus deeper in the Ansible core and affects numerous network device modules; I can't fathom how this could escape the integration tests.

### Long Story Short

I understand why the Ansible team decided to bite the bullet and have their own Windows Longhorn/Vista moment[^WLV], but the many changes in behavior they introduced will be as popular as [Vista's endless security popups](https://blog.codinghorror.com/windows-vista-security-through-endless-warning-dialogs/).

[^WLV]: If you're too young to know what I'm talking about and care about the early history of IT, I can highly recommend the episodes the Acquired podcast did on Microsoft ([part 1](https://www.acquired.fm/episodes/microsoft), [part 2](https://www.acquired.fm/episodes/microsoft-volume-ii), the [Steve Ballmer interview](https://www.acquired.fm/episodes/the-steve-ballmer-interview))

Just the things I discovered so far turn all your Ansible playbooks into ticking time bombs. Can you be sure you found all instances of the non-bool **when** conditions? I [was](https://github.com/ipspace/netlab/pull/2764)... and was [already proven wrong](https://github.com/ipspace/netlab/commit/9de223afbe15ed04dd570901f1be0ab26eaf20cd).
