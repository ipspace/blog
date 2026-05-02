proc usage {} { puts "Syntax: tclsh ifchange.tcl interface \[on|off|change|flap\]";}

proc doConfig { mode cmd } { 
  if { [ catch { ios_config $mode $cmd } errmsg ] } { error "IOS configuration $mode / $cmd failed"; }
}

proc getState { ifnum } {
  if { [ catch { set ifstate [exec "show interface $ifnum"] } iferror ] } {
    error "No such interface: $ifnum";
  }
  set result [expr [ string first {administratively down} $ifstate  ] < 0]
  return $result ;
}

proc changeState { ifnum } {
  puts "changing state of $ifnum" ;
  if { [getState $ifnum] } {
    puts "shut down interface $ifnum" ;
    doConfig "interface $ifnum" "shutdown"; } else {
    puts "enable interface $ifnum" ;
    doConfig "interface $ifnum" "no shutdown"; }
}

proc flapState { ifnum } {
  changeState $ifnum;
  puts "... waiting ...";
  after 6000;
  changeState $ifnum;
}

proc printState { ifnum } {
  if { [getState $ifnum] } { puts "interface is up"; } else { puts "interface is down" }
}

set ifnum [lindex $argv 0]
set ifstate [lindex $argv 1]
if {[string equal $ifnum ""]} { usage; return; }
if {[string equal $ifstate ""]} { 
  if { [ catch { printState $ifnum; } errmsg ] } { puts stderr $errmsg; }
  return; 
}

if { [ catch {
  switch $ifstate {
    on      { doConfig "interface $ifnum" "no shutdown";
              puts "Interface $ifnum changed state to on"; }
    off     { doConfig "interface $ifnum" "shutdown"
              puts "Interface $ifnum changed state to off"; }
    flap    { flapState $ifnum }
    change  { changeState $ifnum }
    default { usage; }
  }
  } errmsg ] } { puts stderr $errmsg; }