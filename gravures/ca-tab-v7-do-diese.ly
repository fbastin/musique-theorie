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
    \new Staff = "haut" { \clef treble \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \new Voice = "md" { \key cis \major <eis' gis' cis''>1 <fis' gis' bis'>1 <eis' gis' cis''>1 \bar "|"  <gis' cis'' eis''>1 <gis' bis' fis''>1 <gis' cis'' eis''>1 \bar "|"  <cis' eis' gis'>1 <bis fis' gis'>1 <cis' eis' gis'>1 \bar "||" \key cis \minor <e' gis' cis''>1 <fis' gis' bis'>1 <e' gis' cis''>1 \bar "|"  <gis' cis'' e''>1 <gis' bis' fis''>1 <gis' cis'' e''>1 \bar "|"  <cis' e' gis'>1 <bis fis' gis'>1 <cis' e' gis'>1 \bar "|." } }
    \new Staff { \clef bass \accidentalStyle forget \set Staff.printKeyCancellation = ##f \omit Staff.TimeSignature \cadenzaOn \key cis \major cis1 gis1 cis1 \bar "|"  cis1 gis1 cis1 \bar "|"  cis1 gis1 cis1 \bar "||" \key cis \minor cis1 gis1 cis1 \bar "|"  cis1 gis1 cis1 \bar "|"  cis1 gis1 cis1 \bar "|." }
    \context Lyrics = "noms" \lyricsto "md" { \markup \tiny \italic "do dièse majeur" _ _ _ _ _ _ _ _ \markup \tiny \italic "do dièse mineur" _ _ _ _ _ _ _ _ }
    \context Lyrics = "positions" \lyricsto "md" { \markup \tiny \italic "octave" _ _ \markup \tiny \italic "tierce" _ _ \markup \tiny \italic "quinte" _ _ \markup \tiny \italic "octave" _ _ \markup \tiny \italic "tierce" _ _ \markup \tiny \italic "quinte" _ _ }
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
