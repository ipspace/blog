title: Use FOR-IF Construct in Jinja2 Loops

A networking engineer attending the [Building Network Automation Solutions](https://www.ipspace.net/Building_Network_Automation_Solutions) online course sent me a solution that included a pretty common (but somewhat suboptimal) way of iterating through a data structure that contains some elements you're not interested in.

Let's assume we have collected ARP entries from a router having a few LAN and WAN interfaces (I removed the MAC addresses for readability reasons):

    arp:
    - intf: Serial0
      addr: 172.16.0.1
    - intf: Gigabit0
      addr: 10.0.0.1
    - intf: Serial1
      addr: 172.16.1.1
    - intf: Gigabit2
      addr: 10.0.1.1

Assuming we're interested in hosts connected to LAN interfaces, we could write a simple Jinja2 template to print out only those ARP entries that have 'Gigabit' in interface name:

    {% for entry in arp %}
    {%   if 'Gigabit' in entry["intf"] %}
    {{ entry["intf"] }},{{ entry["addr"] }}
    {%   endif %}
    {% endfor %}

Now let's add a minor twist to the task: we'd love to have a header and a footer line, but only if there is at least one LAN-attached host (so we can't just print the header and the footer before and after the **for** loop).

The obvious idea would be to use *loop.first* and *loop.last* variables to identify the first and last loop iteration:

    {% for entry in arp %}
    {%   if 'Gigabit' in entry["intf"] %}
    {%     if loop.first %}
    ---- Gigabit Ethernet ARP entries ---
    {%     endif %}
    {{ entry["intf"] }},{{ entry["addr"] }}
    {%     if loop.last %}
    ---- Total {{ loop.length }} entries ---
    {%     endif %}
    {%   endif %}
    {% endfor %}

Now try to figure out what would happen when this bit of code is processing our ARP table.

Here's the spoiler:

* The header would not be printed because Jinja2 would never hit the inner IFs on first loop iteration;
* The total number of entries would be incorrect because the loop iterates over four (not two) ARP entries

While you could work around this challenge with an ingenious use of Jinja2 variables, it's much simpler to fix both problems *and* make your code easier to understand if you combine the element selection conditional expression with the **for** statement:

    {% for entry in arp if 'Gigabit' in entry["intf"] %}
    ...
    {% endfor %}

When using a **for** - **if** construct the loop is executed only when the conditional expression is true, resulting in desired values of loop variables.

The final template is also easier to read and understand:

    {% for entry in arp if 'Gigabit' in entry["intf"] %}
    {%   if loop.first %}
    ---- Gigabit Ethernet ARP entries ---
    {%   endif %}
    {{ entry["intf"] }},{{ entry["addr"] }}
    {%   if loop.last %}
    ---- Total {{ loop.length }} entries ---
    {%   endif %}
    {% endfor %}
