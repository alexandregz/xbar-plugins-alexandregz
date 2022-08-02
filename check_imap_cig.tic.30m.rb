#!/usr/bin/env ruby
# encoding: UTF-8

# <bitbar.title>IMAP check</bitbar.title>
# <bitbar.version>1.0</bitbar.version>
# <bitbar.author>Alexandre Espinosa Menor</bitbar.author>
# <bitbar.author.github>alexandregz</bitbar.author.github>
# <bitbar.desc>Check IMAP account</bitbar.desc>
# <bitbar.image>To Do</bitbar.image>
# <bitbar.dependencies>Rfc2047</bitbar.dependencies>

# config 
IMAP_CONN = {
    "HOST"      => 'pop3.example.gal',
     "USER"      => 'example@example.gal',
     "PASSWORD"  => '12345678'
}


require 'net/imap'
require 'base64'
require 'Rfc2047'

MSGS_TO_SHOW = 10

imap = Net::IMAP.new(IMAP_CONN['HOST'])
imap.login(IMAP_CONN['USER'], IMAP_CONN['PASSWORD'])

imap.examine('INBOX')

# messages = imap.search(["NOT", "DELETED"])
messages_new = imap.search(["UNSEEN"])

messages_seen = imap.search(["SEEN"])

# last 5
messages_seen = messages_seen.sort_by { |number| -number }.take(MSGS_TO_SHOW)

if messages_new.count > 0
    puts "📬 (" + messages_new.count.to_s + ") | color=red"
else
    #puts "📪 no messages"
    puts "📪 (0)"
end
puts "---"

messages_seen.each do |message_id|
  envelope = imap.fetch(message_id, "ENVELOPE")[0].attr["ENVELOPE"]
  subject = envelope.subject.sub(/=\?utf-8\?B\?/i, "")
  subject = Base64.decode64(subject) if(subject != envelope.subject)
  subject = Rfc2047.decode(subject)
  puts "#{envelope.from[0].mailbox}@#{envelope.from[0].host}: \t #{subject}"
end

puts "---"
