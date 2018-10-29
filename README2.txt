####

#   To-do list:
#   - ensure halfbeats are viable
#   - discriminate against capital words
#   - store unknown words into a file to be handled later
#   - create linemakers that don't follow meter

#  GLOSSARY

#  Three prefixes are used to distinguish the dual-layer lines.
#  p - May be thought as the phonetic line, or the printed line. This is what will be shown as end-product
#  q - May be thought as the quantum line, because it enjoins both p and r lines in a sort of superposition to be analyzed separately and together
#  r - May be thought as the retracted or referral line, because it shows what the pLine says alternatively

#  qLine holds two lists. Most of the time, they're the same. They could split,
#  such as when contractions need to be separated, or if there's half-beats, etc.

#  qAnteLine = The line before the one currently being built, but not mutable so it could be reloaded
#  runLine = The line before the one building, but mutable so it can be cut and appended

#  qLineIndexList - Writes the index points for qLine. Starts at highest number (furthest right in sentence) and moves toward zero.
#  proxDicIndexList - Matches with qLineIndexList. Starts at 0 to find the immediate proxList for the furthest right, then the second-right gets index 1, etc.

#  superPopList = The 'list of lists' that holds words to be examined
#  superBlackList - The 'list of lists' that hold words whose paths have already been exhausted,
#      which is necessary to ensure a loop issue of trying and failing the same paths repeatedly

#  redButton = The boolean value that triggers a veto of a line, stanza, or poem that has failed, which resets all values

#  Organization of variables: empLine, qEmpLine, superPopList, rhymeList, qLineIndexList, proxDicIndexList, qWord, qLine, qAnteLine, redButton

