\version "2.24.3"
%% Fichier produit par outils/generer_cadences.py — ne pas modifier à la main.
#(set-global-staff-size 13)
\paper {
  indent = 0
  ragged-right = ##f
  paper-width = 168\mm
  line-width = 166\mm
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new PianoStaff <<
    \new Lyrics = "noms"
    \new Lyrics = "positions"
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "|" \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "|" \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "||" \key ais \minor <cis' eis' ais'>1 <dis' fis' ais'>1 <bis eis' gisis'>1 <cis' eis' ais'>1 \bar "|"  <eis' ais' cis''>1 <fis' ais' dis''>1 <eis' gisis' bis'>1 <eis' ais' cis''>1 \bar "|"  <ais cis' eis'>1 <ais dis' fis'>1 <gisis bis eis'>1 <ais cis' eis'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \hideNotes c1 c1 c1 c1 \unHideNotes \bar "|" \hideNotes c1 c1 c1 c1 \unHideNotes \bar "|" \hideNotes c1 c1 c1 c1 \unHideNotes \bar "||" \key ais \minor ais,1 dis1 eis1 ais,1 \bar "|"  ais,1 dis1 eis1 ais,1 \bar "|"  ais,1 dis1 eis1 ais,1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "la dièse majeur" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "la dièse mineur" _ _ _ _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "—" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #1.0
    }
    \context {
      \Lyrics
      \override LyricText.self-alignment-X = #LEFT
      \override LyricText.extra-spacing-width = #'(+inf.0 . -inf.0)
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #0.2
      \override VerticalAxisGroup.nonstaff-nonstaff-spacing.padding = #0.1
    }
  }
}
