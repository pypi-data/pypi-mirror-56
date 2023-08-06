from lxml import etree, objectify


class TcxActivity(object):
  """
  See https://stackoverflow.com/questions/53319313/iterate-xpath-elements-to-get-individual-elements-instead-of-list
  """

  def __init__(self, file_path, namespace=None):
    # namespace = namespace  \
    #             or 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
    # self.namespaces = {'ns': namespace}
    self.tree = etree.parse(file_path)
    self.root = self.tree.getroot()

    # Strip namespaces.
    for elem in self.root.getiterator():
        if not hasattr(elem.tag, 'find'): continue  # (1)
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]
    objectify.deannotate(self.root, cleanup_namespaces=True)
    #self.activity = self.root.Activities.Activity

    # Verify that this is .tcx
    # if file_path.lower().endswith('.tcx'):

    # Loop through activity trackpoints to create DataFrame rows.
    rows = [[
        tp.findtext('Time'),
        tp.findtext('HeartRateBpm/Value'),
    ] for tp in self.tree.xpath('//Track/Trackpoint')] 
