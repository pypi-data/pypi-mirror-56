
class Splice_Info_Section:    
    def __init__(self):
        self.table_id =Scte35(size='uint:8')
        self.table_id.val=252
        self.section_syntax_indicator = Scte35('bool')
        self.private = Scte35('bool')
        self.reserved= Scte35('uint:2')
        self.section_length = Scte35('uint:12')
        self.protocol_version = Scte35('uint:8')
        self.encrypted_packet =  Scte35('bool')
        self.encryption_algorithm =Scte35('uint:6')
        self.pts_adjustment = Scte35('uint:33')
        self.cw_index = Scte35('uint:8')
        self.tier = Scte35('uint:12')
        self.splice_command_length = Scte35('uint:12')
        self.splice_command_type = Scte35('uint:8')


class Scte35:
    def __init__(self,size,val=None):
        self.size=size
        self.val=val

    def rd(self,mesg):
        self.val=mesg.read(self.size)

    def __repr__(self):
        if self.val : return f'\"{self.size}={self.val}\"'
        return ''

mesg=''		
fu=Scte35('uint:8')
fu.val=252
		
q=Splice_Info_Section()
print(vars(q))

print(fu)