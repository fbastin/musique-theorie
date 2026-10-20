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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key ces \major <ees' ges' ces''>1 <fes' aes' ces''>1 <des' ges' bes'>1 <ees' ges' ces''>1 \bar "|"  <ges' ces'' ees''>1 <aes' ces'' fes''>1 <ges' bes' des''>1 <ges' ces'' ees''>1 \bar "|"  <ces' ees' ges'>1 <ces' fes' aes'>1 <bes des' ges'>1 <ces' ees' ges'>1 \bar "||" \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "|" \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "|" \hideNotes c''1 c''1 c''1 c''1 \unHideNotes \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key ces \major ces1 fes1 ges1 ces1 \bar "|"  ces1 fes1 ges1 ces1 \bar "|"  ces1 fes1 ges1 ces1 \bar "||" \hideNotes c1 c1 c1 c1 \unHideNotes \bar "|" \hideNotes c1 c1 c1 c1 \unHideNotes \bar "|" \hideNotes c1 c1 c1 c1 \unHideNotes \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "do bémol majeur" _ _ _ _ _ _ _ _ _ _ _ \markup \tiny \italic "do bémol mineur" _ _ _ _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "octave" _ _ _ \markup \tiny \italic "tierce" _ _ _ \markup \tiny \italic "quinte" _ _ _ \markup \tiny \italic "—" _ _ _ _ _ _ _ _ _ _ _ }
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
