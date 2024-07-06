---
title: "Running Arista cEOS in GitHub Codespaces"
date: 2024-07-02 07:30:00+0200
tags: [ netlab ]
netlab_tag: codespace
---
[![](/2024/07/container-download.jpg)](/2024/07/container-download.jpg)
{ .sideicon }

Yesterday, I explained how you can [run netlab examples in GitHub codespaces](/2024/07/netlab-examples-codespaces.html) and mentioned that they work best with vendors who understand the value of frictionless downloads. But what if you'd like to use a device from [one of the good guys](/2024/02/netlab-vxlan-labs.html) who provide the container images but require a registration?

It turns out the solution is trivial:
<!--more-->
* Download the image (for example, Arista cEOS) to your laptop
* Drag-and-drop the image from a local file folder to the **Explore** tab of a web page of a running codespace.
* Wait for the upload to complete; the image will probably be waiting in the top directory.
* Install the container image.
* Have fun.

Is there a way to get the image (for example, an Arista cEOS container image) into a codespace without the trip through the laptop? Roman Dodin [published a whole hackathon exercise](https://www.youtube.com/watch?v=KJMVH2okO24) using JavaScript to get it done; it turns out there's a slightly simpler workaround:

* Navigate to the vendor download page and copy the download link.
* Open a new web browser window and make sure the URL is `about:blank` (so you won't get extra requests)
* Open the developer pane (right-click + Inspect in my version of Chrome) and select the **Network** tab.
* Paste the download link and start the download. The last request in the **Network** tab will be the actual download.

{{<figure src="/2024/07/Arista-cEOS-download.png">}}

* Right-click that request and select "Copy as cURL"
* Paste whatever is on the clipboard into the codespaces terminal pane, adding `--output some-file-name.tar.xz`
* Wait for the download to complete, and install the container image with the `docker image import` command.

Now, wouldn't it be brilliant if Arista's website developers could do that for you? All they'd have to do is add the *Copy curl command* to the existing *Copy URL* button that appears next to the image name, and our lives would be much simpler without Arista losing control over who is downloading the image.
