def split_list(thelist, delimiter):
  results = []
  sublist = []
  for item in thelist:
    if item == delimiter:
      results.append(sublist)
      sublist = []
    else:
      sublist.append(item)
  if sublist:
    results.append(sublist)
  return results