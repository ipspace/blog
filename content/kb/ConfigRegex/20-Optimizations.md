---
kb_section: ConfigRegex
minimal_sidebar: true
title: Experiences and Optimizations
url: /kb/ConfigRegex/20-Optimizations.html
---
The Jinja2-only solution was working fine but suffers from poor performance when used on edge switches that have numerous managed client ports (some of my switches have up to 240 ports). The performance of looping over every single regex, parsing the whole configuration and rereading the result was not acceptable, so I optimized the configuration management by implementing two Jinja2 filters in Python. These filters work much faster than Ansible loops I used in the original solution.

## Filter: ios\_config\_section\_extract

This filter is used to extract a configuration section and optionally save it into a file. Here's how you could use it:

    - set_fact:
        src_config: >
          {{ src_config | ios_config_section_extract(regexp,
                             ignorecase, prefix_str, filename) }}

### Input

The input (**src\_config**) can be either a single string with line separators or a list of strings.

### Parameters

|Parameter|Required|Default|Description|
|---|---|---|---|
|regexp| Yes | | A list of strings or a single string containing the regular expressions to select the configuration sections. Line start marker '^' or line end marker '$' are set by the filter when they're omitted. This ensures that the filter will (for example) match only interface configuration even when you pass plain interface name as the parameter.|
|ignorecase| No | false | If set to true, the regex is case-insensitive.|
|prefix_str| No  | '' | Allows to prepend a common string to the all regular expression. This string will be directly prepended to every regular expression before the missing line-start and -end markers are added. For example, you can extract VLAN configurations if you pass the list of VLAN numbers as **regexp** parameter and 'vlan' as **prefix_str**.|
|filename| No | '' | If a filename is specified, the selected configurations will be saved as a textfile. The directory must exist.|
{.fmtTable}

### Result

* Selected configuration: list of strings
* Textfile: if the filename parameter was specified, the textfile will contain the selected configuration sections

## Filter: ios\_config\_section\_remove

This filter deletes parts of device configuration. Here's the simplest way to use it:

    - name: Remove all blocks or commands defined in delete_section_regex
      set_fact:
        src_config: >
          {{ src_config |
               ios_config_section_remove(delete_section_regex) }}

This filter has the same input and parameters as the **ios\_config\_section\_extract** filter and returns the contents of input configuration after deleting all configuration sections matched by regular expressions.
