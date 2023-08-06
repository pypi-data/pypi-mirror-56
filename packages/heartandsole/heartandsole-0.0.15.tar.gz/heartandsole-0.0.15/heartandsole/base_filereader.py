from lxml import etree, objectify


# Set to True to add a column to the DataFrame indicating whether a row would
# have been removed if removal of stopped periods were enabled, but don't
# actually remove it.
DEBUG_EXCISE = False


class BaseFileReader(object):
  """Base class for file readers."""
  def __init__(self):
    """Instantiates a BaseFileReader.

    Args:
    #   file_obj: A file-like object representing an activity file.
    """
    # TO ACTIVITY
    self._remove_stopped_periods = remove_stopped_periods or DEBUG_EXCISE

    # Keep in class for now, but consider making a global variable.
    field_names = ['timestamp', 'distance', 'speed', 'elevation',
                   'lat', 'lon', 'heart_rate', 'cadence',
                   'running_smoothness', 'stance_time', 'vertical_oscillation']
    #field_names = ['timestamp', 'distance', 'enhanced_speed', 'enhanced_altitude',
    #          'position_lat', 'position_long', 'heart_rate', 'cadence',
    #          'running_smoothness', 'stance_time', 'vertical_oscillation']

    #records = list(self.get_records())

    # Memoize for use in subclasses and methods. Must be initialized
    # by subclasses.
    self.start_time = None
    self.end_time = None
    self.elapsed_time = None

  def build_dataframe(self):  #, rows, blocks, time_offsets):
    """Constructs a time series DataFrame of activity data.

    Args:
      rows: A list of length n_time made up of equal-length lists 
            which define values of each field at each row's timestep.
      blocks: A list of ints, length n_time, which defines a block index
              for the DataFrame. Each block represents a period of
              movement, as defined by the start/stop buttons on the
              device.
      time_offsets: A list of datetime.timedeltas, length n_time, which
                    defines a timedelta index for the DataFrame. Each 
                    index is the elapsed time since the start of the
                    activity.
    """
    # Check that lists of data are formatted correctly.
    assert len(blocks) == len(time_offsets)

    if DEBUG_EXCISE:
      self.field_names += ['excise']

    # Build the DataFrame
    self.data = pandas.DataFrame(self.rows, columns=field_names,
                                 index=[self.blocks, self.time_offsets])
    self.data.index.names = ['block', 'offset']

    # Fields may not exist in all files (except timestamp),
    # so drop the columns if they're not present.
    for field in self.field_names:
      if self.data[self.data[field].notnull()].empty:
        self.data.drop(field, axis=1, inplace=True)

    # Clean up position data, if it exists.
    if self.has_position:
      self.data['position_long'].fillna(method='bfill', inplace=True)
      self.data['position_lat'].fillna(method='bfill', inplace=True)

  def get_records(self):
    """Returns an iterable of records or trackpoints."""
    raise NotImplementedError('Subclasses must implement this method.')


class TcxFileReader(BaseFileReader):
  """
  See https://stackoverflow.com/questions/53319313/iterate-xpath-elements-to-get-individual-elements-instead-of-list
  """

  FIELD_NAME_DICT = {
      'timestamp': 'Time',
      'distance': 'DistanceMeters',
      'speed': 'Extensions/TPX/Speed',
      'elevation': 'AltitudeMeters',
      'lat': 'Position/LatitudeDegrees',
      'lon': 'Position/LongitudeDegrees',
      'heart_rate': 'HeartRateBpm/Value',
      'cadence': 'Extensions/TPX/RunCadence',
      'running_smoothness': None,             # TBD 
      'stance_time': None,                    # TBD
      'vertical_oscillation': None,           # TBD
  }

  def __init__(self, file_path, namespace=None):
    self.tree = etree.parse(file_path)
    self.root = self.tree.getroot()

    # Strip namespaces.
    for elem in self.root.getiterator():
      if not hasattr(elem.tag, 'find'): continue 
      i = elem.tag.find('}')
      if i >= 0:
        elem.tag = elem.tag[i+1:]
    objectify.deannotate(self.root, cleanup_namespaces=True)

    # Verify that this is .tcx
    # if file_path.lower().endswith('.tcx'):

  def get_records(self):
    """Retrieves a list of trackpoints from the .tcx file."""
    field_names = [val for val in self.FIELD_NAME_DICT.values() 
                   if val is not None]

    # nlaps = number of lap button presses + 1 (starts with 1)
    print('Number of laps: %d' % len(tree.xpath('//Lap'))) 
    # One track per lap min. Each lap's track number reflects 
    # number of pauses + 1.
    print('Number of tracks: %d' % len(tree.xpath('//Track'))) 

    # Loop through activity trackpoints to create DataFrame rows.
    records = []
    trackpoints = self.tree.xpath('//Track/Trackpoint')
    for tp in trackpoints[3:5]:
      curr_timestamp = tp.findtext('Time')
      # time_offsets.append(curr_timestamp - tcx.start_time)
      for field in field_names:
        print('%s: %s' % (field, tp.findtext(field)))
        #print('%s: %s' % (field, tp.find(field)))
        #print(dir(tp.find(field)))

  return records 
