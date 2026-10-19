\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
  ragged-right = ##t
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
  <<
    \new Staff <<
      \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature
        \time 6/8 c''8[ d''8 e''8] f''8[ e''8 d''8] | \time 9/8 c''8[ d''8 e''8] f''8[ g''8 a''8] g''8[ f''8 e''8] | \time 12/8 c''4. d''4. e''4. c''4.
        \bar "|."
      }
      \new NullVoice = "temps" { b'4. b'4. b'4. b'4. b'4. b'4. b'4. b'4. b'4. }
    >>
    \new Lyrics \with { \override LyricText.font-size = #-1 } \lyricsto "temps" { "1" "2" "1" "2" "3" "1" "2" "3" "4" }
  >>
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
