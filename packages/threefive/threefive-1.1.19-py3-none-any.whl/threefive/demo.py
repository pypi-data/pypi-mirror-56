mesg='/DA0AAAAAAAA///wBQb+cr0AUAAeAhxDVUVJSAAAjn/PAAGlmbAICAAAAAAsoKGKNAIAmsnRfg=='

out='''Decoded length = 55, Table ID = 0xFC, MPEG Short Section, Not Private, Reserved = 0x3,
 Section Length = 52, Protocol Version = 0, unencrypted Packet, PTS Adjustment = 0x000000000,
  Tier = 0xfff'''
out1=''' Splice Command Length = 0x5, Time Signal, Time = 0x072bd0050 - 21388.766756,
   Descriptor Loop Length = 30'''
out2=''' Segmentation Descriptor - Length=28, 
   Segmentation Event ID = 0x4800008e, Segmentation Event Cancel Indicator NOT set, 
   Delivery Not Restricted flag = 0, Web Delivery Allowed flag = 0, 
   No Regional Blackout flag = 1, Archive Allowed flag = 1, Device Restrictions = 3, 
   Program Segmentation flag SET, Segmentation Duration = 0x0001a599b0 = 307.000000 seconds, 
   UPID Type = Turner Identifier length = 8, Turner Identifier = 0x000000002ca0a18a, 
   Type = Placement Opportunity Start, Segment num = 2 Segments Expected = 0, 
   CRC32 = 0x9ac9d17e
   '''
import  threefive

tf=threefive.Splice(mesg)
tf.show_info_section()
print(out)
tf.show_command()
print(out1)
tf.show_descriptors()
print(out2)
   